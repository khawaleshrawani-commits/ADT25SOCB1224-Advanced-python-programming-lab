from datetime import datetime
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional


# ============================================================
# Formatter Registry
# ============================================================

FORMATTERS: Dict[str, Callable[[Any], str]] = {}


def formatter(name: str):
    """
    Decorator used to register a custom formatter.

    Example:
        @formatter("uppercase")
        def uppercase(value):
            return str(value).upper()
    """
    def decorator(func: Callable[[Any], str]):
        FORMATTERS[name] = func
        return func

    return decorator


# ============================================================
# Built-in Formatters
# ============================================================

@formatter("uppercase")
def uppercase(value: Any) -> str:
    return str(value).upper()


@formatter("lowercase")
def lowercase(value: Any) -> str:
    return str(value).lower()


@formatter("title")
def title_case(value: Any) -> str:
    return str(value).title()


@formatter("currency")
def currency(value: Any) -> str:
    return f"${float(value):,.2f}"


@formatter("percentage")
def percentage(value: Any) -> str:
    return f"{float(value) * 100:.2f}%"


@formatter("number")
def number(value: Any) -> str:
    return f"{float(value):,.2f}"


@formatter("date")
def format_date(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            return value

    return str(value)


# ============================================================
# Report Template
# ============================================================

class ReportTemplate:
    """
    Represents a reusable report template.
    """

    def __init__(
        self,
        name: str,
        template: str,
        formatters: Optional[Dict[str, List[str]]] = None
    ):
        self.name = name
        self.template = template
        self.formatters = formatters or {}

    def add_formatter(self, field: str, *formatter_names: str):
        """
        Dynamically attach formatters to a field.
        """
        self.formatters.setdefault(field, []).extend(formatter_names)
        return self

    def format_value(self, field: str, value: Any) -> str:
        """
        Apply all configured formatters to a field.
        """
        result = value

        for formatter_name in self.formatters.get(field, []):
            if formatter_name not in FORMATTERS:
                raise ValueError(
                    f"Unknown formatter: {formatter_name}"
                )

            result = FORMATTERS[formatter_name](result)

        return str(result)

    def render(self, data: Dict[str, Any]) -> str:
        """
        Render the template with supplied data.
        """

        class SafeDict(dict):
            def __missing__(self, key):
                return f"{{{key}}}"

        formatted_data = {
            field: self.format_value(field, value)
            for field, value in data.items()
        }

        return self.template.format_map(SafeDict(formatted_data))

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"ReportTemplate("
            f"name={self.name!r}, "
            f"template={self.template!r})"
        )


# ============================================================
# Report
# ============================================================

class Report:
    """
    Represents a generated report.
    """

    def __init__(
        self,
        title: str,
        content: str,
        data: Optional[Dict[str, Any]] = None
    ):
        self.title = title
        self.content = content
        self.data = data or {}

    # --------------------------------------------------------
    # Class Method
    # --------------------------------------------------------

    @classmethod
    def from_template(
        cls,
        template: ReportTemplate,
        data: Dict[str, Any],
        title: Optional[str] = None
    ):
        """
        Factory method for generating a report from a template.
        """
        content = template.render(data)

        return cls(
            title=title or template.name,
            content=content,
            data=data
        )

    # --------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------

    def __str__(self):
        return f"{self.title}\n{'=' * len(self.title)}\n{self.content}"

    def __len__(self):
        return len(self.content)

    def __iter__(self) -> Iterator[str]:
        return iter(self.content.splitlines())

    def __getitem__(self, key):
        """
        Allows report["title"], report["content"], etc.
        """
        if key == "title":
            return self.title

        if key == "content":
            return self.content

        if key == "data":
            return self.data

        raise KeyError(key)

    def __add__(self, other):
        """
        Combine two reports.
        """
        if not isinstance(other, Report):
            return NotImplemented

        combined_title = f"{self.title} + {other.title}"

        combined_content = (
            self.content
            + "\n\n"
            + other.content
        )

        combined_data = {
            **self.data,
            **other.data
        }

        return Report(
            combined_title,
            combined_content,
            combined_data
        )

    def save(self, filename: str):
        """
        Save report to a text file.
        """
        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(self))

    def __repr__(self):
        return (
            f"Report("
            f"title={self.title!r}, "
            f"length={len(self)})"
        )


# ============================================================
# Report Generator
# ============================================================

class ReportGenerator:
    """
    Central manager for templates and generated reports.
    """

    def __init__(self):
        self.templates: Dict[str, ReportTemplate] = {}
        self.reports: List[Report] = []

    def register_template(self, template: ReportTemplate):
        self.templates[template.name] = template
        return self

    def create_report(
        self,
        template_name: str,
        data: Dict[str, Any],
        title: Optional[str] = None
    ) -> Report:

        if template_name not in self.templates:
            raise KeyError(
                f"Template '{template_name}' not found."
            )

        template = self.templates[template_name]

        report = Report.from_template(
            template,
            data,
            title
        )

        self.reports.append(report)

        return report

    def __getitem__(self, template_name: str):
        """
        Allows:
            generator["sales"]
        """
        return self.templates[template_name]

    def __len__(self):
        return len(self.reports)

    def __iter__(self):
        return iter(self.reports)

    def __repr__(self):
        return (
            f"ReportGenerator("
            f"templates={len(self.templates)}, "
            f"reports={len(self.reports)})"
        )


# ============================================================
# Custom Formatter Example
# ============================================================

@formatter("stars")
def stars(value: Any) -> str:
    """
    Custom formatter created by the user.
    """
    return f"★ {value} ★"


@formatter("signed")
def signed(value: Any) -> str:
    """
    Add + / - sign to numbers.
    """
    number = float(value)

    if number >= 0:
        return f"+{number:.2f}"

    return f"{number:.2f}"


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":

    generator = ReportGenerator()

    # --------------------------------------------------------
    # Define a user-customizable template
    # --------------------------------------------------------

    sales_template = ReportTemplate(
        name="sales",
        template="""
Sales Report
------------

Salesperson : {name}
Department  : {department}
Revenue     : {revenue}
Growth      : {growth}
Performance : {performance}
Report Date : {date}
""".strip()
    )

    # --------------------------------------------------------
    # Dynamically configure formatting
    # --------------------------------------------------------

    sales_template \
        .add_formatter("name", "title") \
        .add_formatter("department", "uppercase") \
        .add_formatter("revenue", "currency") \
        .add_formatter("growth", "percentage") \
        .add_formatter("performance", "stars") \
        .add_formatter("date", "date")

    # Register template
    generator.register_template(sales_template)

    # --------------------------------------------------------
    # Input data
    # --------------------------------------------------------

    sales_data = {
        "name": "john smith",
        "department": "sales",
        "revenue": 125000.50,
        "growth": 0.153,
        "performance": "Excellent",
        "date": "2026-08-31"
    }

    # --------------------------------------------------------
    # Generate report
    # --------------------------------------------------------

    report = generator.create_report(
        "sales",
        sales_data,
        title="Monthly Sales Report"
    )

    print(report)

    # --------------------------------------------------------
    # Magic methods
    # --------------------------------------------------------

    print("\nReport length:", len(report))

    print("Report title:", report["title"])

    print("\nReport lines:")
    for line in report:
        print(line)

    # --------------------------------------------------------
    # Generate another report
    # --------------------------------------------------------

    employee_template = ReportTemplate(
        name="employee",
        template="""
Employee Report
---------------

Name   : {name}
Role   : {role}
Salary : {salary}
""".strip()
    )

    employee_template \
        .add_formatter("name", "title") \
        .add_formatter("role", "uppercase") \
        .add_formatter("salary", "currency")

    generator.register_template(employee_template)

    employee_report = generator.create_report(
        "employee",
        {
            "name": "alice johnson",
            "role": "software engineer",
            "salary": 95000
        }
    )

    print("\n" + str(employee_report))

    # --------------------------------------------------------
    # Combine reports using __add__
    # --------------------------------------------------------

    combined = report + employee_report

    print("\nCombined Report")
    print("===============")
    print(combined)

    # --------------------------------------------------------
    # Generator magic methods
    # --------------------------------------------------------

    print("\nNumber of generated reports:", len(generator))

    print("\nAvailable reports:")
    for generated_report in generator:
        print("-", generated_report.title)

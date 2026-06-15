from datetime import datetime
from decimal import Decimal

from langchain.tools import BaseTool, tool
from langgraph.prebuilt.tool_node import ToolRuntime
from sqlalchemy import func, select

from database.models.spent_model import SpentModel


def _get_config_session_maker(runtime: ToolRuntime):
    configurable = runtime.config.get("configurable", {})
    session_maker = configurable.get("session_maker")
    if not session_maker:
        raise RuntimeError("session_maker nao encontrado na configuracao da tool.")

    return session_maker


def _get_config_user_id(runtime: ToolRuntime) -> str | None:
    configurable = runtime.config.get("configurable", {})
    return configurable.get("user_id")


def _parse_spent_date(date: str | None) -> datetime | None:
    if not date:
        return None

    normalized_date = date.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized_date)


def _money(value: Decimal | float | int | None) -> str:
    amount = Decimal(value or 0).quantize(Decimal("0.01"))
    return f"R$ {amount}"


def _month_range(month: int | None, year: int | None) -> tuple[datetime, datetime]:
    now = datetime.now()
    selected_month = month or now.month
    selected_year = year or now.year

    start = datetime(selected_year, selected_month, 1)
    if selected_month == 12:
        end = datetime(selected_year + 1, 1, 1)
    else:
        end = datetime(selected_year, selected_month + 1, 1)

    return start, end


@tool
async def add_spent(
    shop_name: str,
    cost: float,
    category: str,
    runtime: ToolRuntime,
    date: str | None = None,
) -> str:
    """Adiciona um novo gasto do usuario logado.

    Use quando o usuario disser que gastou, comprou, pagou ou quiser registrar
    uma despesa. Informe shop_name, cost e category. A data e opcional e deve
    estar em formato ISO, por exemplo 2026-06-15T14:30:00.
    """
    user_id = _get_config_user_id(runtime)
    if not user_id:
        return "Nao consegui identificar o usuario para registrar o gasto."

    spent_date = _parse_spent_date(date)
    spent = SpentModel(
        user_id=user_id,
        shop_name=shop_name.strip(),
        cost=Decimal(str(cost)),
        category=category.strip().lower(),
    )

    if spent_date:
        spent.date = spent_date

    session_maker = _get_config_session_maker(runtime)
    async with session_maker() as session:
        session.add(spent)
        await session.commit()
        await session.refresh(spent)

    return (
        "Gasto registrado com sucesso: "
        f"id={spent.id}, local={spent.shop_name}, valor={_money(spent.cost)}, "
        f"categoria={spent.category}, data={spent.date:%d/%m/%Y}."
    )


@tool
async def get_month_spents(
    runtime: ToolRuntime,
    month: int | None = None,
    year: int | None = None,
) -> str:
    """Retorna todos os gastos do usuario no mes informado, incluindo total.

    Use quando o usuario pedir gastos do mes, extrato, resumo mensal ou total
    gasto. Se mes e ano nao forem informados, consulta o mes atual.
    """
    user_id = _get_config_user_id(runtime)
    if not user_id:
        return "Nao consegui identificar o usuario para buscar os gastos."

    start, end = _month_range(month, year)
    session_maker = _get_config_session_maker(runtime)
    async with session_maker() as session:
        result = await session.execute(
            select(SpentModel)
            .where(
                SpentModel.user_id == user_id,
                SpentModel.date >= start,
                SpentModel.date < end,
            )
            .order_by(SpentModel.date.asc())
        )
        spents = result.scalars().all()

        total_result = await session.execute(
            select(func.coalesce(func.sum(SpentModel.cost), 0)).where(
                SpentModel.user_id == user_id,
                SpentModel.date >= start,
                SpentModel.date < end,
            )
        )
        total = total_result.scalar_one()

    if not spents:
        return f"Nenhum gasto encontrado em {start:%m/%Y}. Total: R$ 0.00."

    lines = [
        f"Gastos de {start:%m/%Y}:",
        *[
            (
                f"- {spent.date:%d/%m}: {spent.shop_name} | "
                f"{spent.category} | {_money(spent.cost)}"
            )
            for spent in spents
        ],
        f"Total do mes: {_money(total)}.",
    ]

    return "\n".join(lines)


@tool
async def get_financial_tips(
    runtime: ToolRuntime,
    month: int | None = None,
    year: int | None = None,
) -> str:
    """Analisa os gastos do mes e retorna dicas financeiras praticas.

    Use quando o usuario pedir conselhos, dicas, analise financeira, onde
    economizar ou como melhorar a vida financeira.
    """
    user_id = _get_config_user_id(runtime)
    if not user_id:
        return "Nao consegui identificar o usuario para analisar os gastos."

    start, end = _month_range(month, year)
    session_maker = _get_config_session_maker(runtime)
    async with session_maker() as session:
        result = await session.execute(
            select(
                SpentModel.category,
                func.count(SpentModel.id),
                func.coalesce(func.sum(SpentModel.cost), 0),
            )
            .where(
                SpentModel.user_id == user_id,
                SpentModel.date >= start,
                SpentModel.date < end,
            )
            .group_by(SpentModel.category)
            .order_by(func.sum(SpentModel.cost).desc())
        )
        categories = result.all()

    if not categories:
        return (
            f"Ainda nao ha gastos registrados em {start:%m/%Y}. "
            "Sugira ao usuario registrar despesas por alguns dias e separar "
            "por categorias como mercado, transporte, lazer, contas e delivery."
        )

    total = sum(Decimal(row[2]) for row in categories)
    biggest_category, biggest_count, biggest_total = categories[0]
    biggest_percent = (Decimal(biggest_total) / total * 100).quantize(Decimal("0.1"))

    category_lines = [
        f"- {category}: {_money(category_total)} em {count} registro(s)"
        for category, count, category_total in categories
    ]

    return "\n".join(
        [
            f"Analise de {start:%m/%Y}. Total gasto: {_money(total)}.",
            "Gastos por categoria:",
            *category_lines,
            (
                f"Maior foco de economia: {biggest_category}, com "
                f"{_money(biggest_total)} ({biggest_percent}% do total) "
                f"em {biggest_count} registro(s)."
            ),
            "Dicas sugeridas:",
            "- Defina um limite semanal para a categoria com maior gasto.",
            "- Separe despesas fixas de variaveis antes de cortar gastos.",
            "- Revise compras pequenas recorrentes; elas costumam pesar no total.",
            "- Reserve uma parte do dinheiro assim que receber, antes dos gastos do mes.",
        ]
    )


TOOLS: list[BaseTool] = [add_spent, get_month_spents, get_financial_tips]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}

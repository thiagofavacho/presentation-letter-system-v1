import re

from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    HRFlowable,
)

from app.models import Promoter, Store

ASSETS_DIR = "app/static/letter_assets"
LOGO_EVER = f"{ASSETS_DIR}/logo_ever.png"
LOGO_TIROLEZ = f"{ASSETS_DIR}/logo_tirolez.jpg"
CARIMBO_SB = f"{ASSETS_DIR}/carimbo_sb.jpeg"

COMPANY_CITY = "São Paulo"
COMPANY_NAME = "SB SERVIÇOS TEMPORARIOS LTDA"

MESES_PT = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def _format_date_pt(date: datetime) -> str:
    return f"{date.day} de {MESES_PT[date.month]} de {date.year}"


def generate_letter_pdf(promoter: Promoter, store: Store, letter_date: datetime) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.8 * cm,
        bottomMargin=0.6 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    body_style = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
    )
    bold_style = ParagraphStyle(
        "Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    
    footer_style = ParagraphStyle(
        "Footer",
        parent=body_style,
        fontSize=10,
        leading=12,
        spaceAfter=0,
    )

    signature_name_style = ParagraphStyle(
        "SignatureName",
        parent=footer_style,
        alignment=TA_CENTER,
    )
    
    store_style = ParagraphStyle(
    "Store",
    parent=body_style,
    spaceAfter=2,
    leading=13,
)

    elements = []

    header_table = Table(
        [[
            Image(LOGO_EVER, width=4.17 * cm, height=1.7 * cm),
            Image(LOGO_TIROLEZ, width=3.15 * cm, height=1.7 * cm),
        ]],
        colWidths=[doc.width / 2, doc.width / 2],
    )
    header_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.15 * cm))

    elements.append(Paragraph(
        f"{COMPANY_CITY}, {_format_date_pt(letter_date)}",
        bold_style,
    ))
    elements.append(Spacer(1, 1.1 * cm))

    store_address = (store.address or "").strip()
    store_neighborhood = (store.neighborhood or "").strip()
    store_city = (store.city or "").strip()
    store_state = (store.state or "").strip().upper()

    city_state = ""

    if store_city and store_state:
        city_state = f"{store_city}/{store_state}"
    elif store_city:
        city_state = store_city
    elif store_state:
        city_state = store_state

    address_parts = [
        store_address,
        store_neighborhood,
        city_state,
    ]

    store_address_line = " - ".join(
        part for part in address_parts if part
    )

    elements.append(
        Paragraph(
            f"AO {store.client or ''}",
            store_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>LOJA: {store.name}</b>",
            store_style
        )
    )

    elements.append(
        Paragraph(
            store_address_line,
            store_style
        )
    )

    elements.append(Spacer(1, 0.6 * cm))

    admission_str = (
        promoter.admission_date.strftime("%d/%m/%Y")
        if promoter.admission_date else "-"
    )
    
    ctps_formatted = re.sub(
    r"\s*,\s*",
    "/ ",
    promoter.ctps or "-",
    )
    
    promoter_address = (promoter.address or "").strip()
    promoter_neighborhood = (promoter.neighborhood or "").strip()
    promoter_city = (promoter.city or "").strip()
    promoter_state = (promoter.state or "").strip().upper()
    promoter_cep = (promoter.cep or "").strip()

    promoter_city_state = ""

    if promoter_city and promoter_state:
        promoter_city_state = f"{promoter_city}/{promoter_state}"
    elif promoter_city:
        promoter_city_state = promoter_city
    elif promoter_state:
        promoter_city_state = promoter_state

    promoter_address_parts = [
        promoter_address,
        promoter_neighborhood,
        promoter_city_state,
    ]

    if promoter_cep:
        promoter_address_parts.append(
            f"CEP: {promoter_cep}"
        )

    promoter_full_address = " - ".join(
        part for part in promoter_address_parts if part
    )

    if not promoter_full_address:
        promoter_full_address = "-"


    paragraph_1 = (
        f"A {COMPANY_NAME}, vem por meio desta, comunicar que seu empregado "
        f"Sr.(a) <b>{promoter.name}</b>, registrado com a matrícula {promoter.employee_id} "
        f"e portador(a) do RG número: {promoter.rg or '-'}, inscrito(a) sob o CPF número "
        f"{promoter.cpf or '-'}, CTPS número {ctps_formatted}, PIS número {promoter.pis or '-'}, "
        f"residente e domiciliado(a) em {promoter_full_address or '-'}, admitido em {admission_str}, "
        f"que executará a função de {promoter.position} por período {promoter.period}, "
        f"dentro do estabelecimento acima mencionado."
    )
    elements.append(Paragraph(paragraph_1, body_style))

    paragraph_2 = (
        "Informamos que o referido empregado participou do treinamento referente ao uso "
        "do(s) EPI(s) e às Normas de Segurança do Trabalho, e está ciente do uso obrigatório "
        "dos Equipamentos de Proteção Individual, conforme Lei nº 514 de 22/12/1977 artigo 158. "
        "Assim como, possui ASO vigente e correspondente às atividades exercidas pelo mesmo e "
        "Curso de Manipulação de Alimentos (requerido apenas para prestadores e serviços da "
        "cafetaria e recomendado para prestadores de frios e Hortifruti)."
    )
    elements.append(Paragraph(paragraph_2, body_style))

    paragraph_3 = (
        f"Declaramos que o referido empregado acima citado exercerá exclusivamente as "
        f"atividades inerentes ao cargo {promoter.position} da {COMPANY_NAME} não possuindo "
        f"qualquer vínculo empregatício com a empresa de V.Sa., sendo de inteira responsabilidade "
        f"da {COMPANY_NAME} todos os encargos trabalhistas, previdenciários, securitários ou "
        f"qualquer que venha a existir."
    )
    elements.append(Paragraph(paragraph_3, body_style))

    paragraph_4 = (
        f"{COMPANY_NAME} garante ainda que, caso V.Sa. empresa venha sofrer qualquer "
        f"fiscalização do Ministério do Trabalho, encaminhará todos os documentos necessários "
        f"do {promoter.position} em referência, tais como contrato de trabalho, ASO admissional "
        f"etc. para comprovar a regularização e conformidade com a legislação trabalhista."
    )
    elements.append(Paragraph(paragraph_4, body_style))

    elements.append(Spacer(1, 0.35 * cm))

    elements.append(Paragraph("Atenciosamente,", footer_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Primeiro nome, abaixo de “Atenciosamente”.
    elements.append(Paragraph(f"<b>{COMPANY_NAME}</b>", footer_style))
    elements.append(Spacer(1, 2 * cm))

    stamp_image = Image(CARIMBO_SB, width=5 * cm, height=2.85 * cm)

    stamp_table = Table(
        [[stamp_image]],
        colWidths=[8 * cm],
        hAlign="LEFT",
    )

    stamp_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(stamp_table)

    elements.append(Spacer(1, 0.35 * cm))
    
    elements.append(HRFlowable(
        width=8 * cm,
        thickness=0.8,
        color="black",
        hAlign="LEFT",
        spaceAfter=0,
    ))
    
    elements.append(Spacer(1, 0.3 * cm))

    # Segundo nome, centralizado em relação à linha de 8 cm.
    signature_name_table = Table(
        [[Paragraph(f"<b>{COMPANY_NAME}</b>", signature_name_style)]],
        colWidths=[8 * cm],
        hAlign="LEFT",
    )

    signature_name_table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(signature_name_table)

    doc.build(elements)

    return buffer.getvalue()
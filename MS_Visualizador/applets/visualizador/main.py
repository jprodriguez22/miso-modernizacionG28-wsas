from dotenv import dotenv_values
from .src.planos import Plano
from .src.lecciones import LeccionesAprendidas
from .src.alertas_ordenes import AlertasOrdenes


# Función
def main(
    *args,
    orden: str = None,
    caracteristicas: str = None,
    puesto_trabajo: str = None,
    zfer: str = None,
    **kwargs
):
    # Definición de variables
    credentials_cal = dotenv_values("./calendario.env")
    credentials_sap = dotenv_values("./sap_ing.env")
    credentials_sf = dotenv_values("./smartfactory.env")
    web_domain = dotenv_values("./conf.env")["API_DOMAIN"]
    driver = dotenv_values("./conf.env")["DRIVERWIN"]
    credentials_cal["DRIVER"] = driver
    credentials_sap["DRIVER"] = driver
    credentials_sf["DRIVER"] = driver
    planos = Plano(credentials_sap=credentials_sap, credentials_cal=credentials_cal)
    lecciones = LeccionesAprendidas(dominio=web_domain, credentials_sf=credentials_sf)
    alertas_ordenes = AlertasOrdenes()

    if args[0] == "actualizar_planos":
        return planos.actualizar_planos()

    if args[0] == "consultar_plano":
        return planos.consultar_plano(orden)

    if args[0] == "consultar_informacion_orden":
        return planos.consultar_info_orden(orden)

    if args[0] == "consultar_caracteristicas_orden":
        return lecciones.consultar_caracteristicas_orden(orden)

    if args[0] == "actualizar_lecciones":
        return lecciones.actualizar_lecciones_aprendidas()

    if args[0] == "consultar_lecciones":
        if caracteristicas:
            caracteristicas = caracteristicas.replace(" ", "").split(",")
        return lecciones.extraer_lecciones_aprendidas(
            caracteristicas=caracteristicas, puesto_trabajo=puesto_trabajo, zfer=zfer
        )

    if args[0] == "imagen_leccion":
        id_leccion = kwargs["id_leccion"]
        return lecciones.extraer_imagen_leccion(id_leccion)

    if args[0] == "encolar_reporte":
        msg = kwargs["alert_message"]
        return alertas_ordenes.send_message(msg)

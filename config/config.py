SIH_DTYPES = {
    'Cuenca': 'object',
    'Asignación_o_Contrato': 'object',
    'Nombre_del_pozo': 'object',
    'Petróleo_(Mbd)': 'float64',
    'Gas_asociado_(MMpcd)': 'float64',
    'Gas__no_asociado_(MMpcd)': 'float64',
    'Agua_(Mbd)': 'float64',
    'Condensado_(Mbd)': 'float64'
}

SIH_PROD_NAMES = {
    'Fecha': 'fecha',
    'Cuenca': 'cuenca',
    'Asignación_o_Contrato': 'asignacion_contrato',
    'Nombre_del_pozo': 'nombre_pozo',
    'Petróleo_(Mbd)': 'petroleo_mbd',
    'Gas_asociado_(MMpcd)': 'gas_asociado_mmpcd',
    'Gas_no_asociado_(MMpcd)': 'gas_no_asociado_mmpcd',
    'Agua_(Mbd)': 'agua_mbd',
    'Condensado_(Mbd)': 'condensado_mbd'
}

CNH_MAP_DTYPES = {
    'POZO': 'object',
    'CAMPO': 'object',
    'ENTIDAD': 'object',
    'UBICACIóN': 'object',
    'CLASIFICACIóN': 'object',
    'ESTADO ACTUAL': 'object',
    'TIPO DE HIDROCARBURO': 'object',
    'FECHA INICIO DE PERFORACIóN': 'object',
    'FECHA FIN PERFORACIóN': 'object',
    'PROFUNDIDAD TOTAL': 'float64',
    'PROFUNDIDAD VERTICAL': 'float64',
    'TRAYECTORIA': 'object',
    'DISPONIBLE': 'object'
}

CNH_MAP_NAMES = {
    'POZO': 'nombre_pozo',
    'CAMPO': 'campo',
    'ENTIDAD': 'entidad',
    'UBICACIóN': 'ubicacion',
    'CLASIFICACIóN': 'clasificacion',
    'ESTADO ACTUAL': 'edo_actual',
    'TIPO DE HIDROCARBURO': 'tipo_hidrocarburo',
    'PROFUNDIDAD TOTAL': 'prof_total',
    'PROFUNDIDAD VERTICAL': 'prof_vertical',
    'TRAYECTORIA': 'trayectoria',
    'DISPONIBLE': 'disponible',
    'FECHA INICIO PERFORACIóN': 'fecha_inicio',
    'FECHA FIN PERFORACIóN': 'fecha_fin'
}

CNH_HC_TYPE = {
    'ACEITE':1,
    'ACEITE-GAS':1,
    'ACEITE Y GAS':1,
    'ACEITE SUPERLIGERO':1,
    'ACEITE LIGERO':1,
    'ACEITE NEGRO':1,
    'GAS':0,
    'GAS-CONDENSADO':0,
    'CONDENSADO':0,
    'GAS SECO':0,
    'GAS HUMEDO':0,
    'GAS Y CONDENSADO':0,
    'NO IDENTIFICADO':0
}

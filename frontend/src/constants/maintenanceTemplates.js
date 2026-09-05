export const MAINTENANCE_TEMPLATES = {
  engine: [
    { id: 'oil_change', label: 'Замена моторного масла и масляного фильтра' },
    { id: 'air_filter', label: 'Замена воздушного фильтра' },
    { id: 'spark_plugs', label: 'Замена свечей зажигания' },
    { id: 'valve_adjustment', label: 'Регулировка клапанов' },
    { id: 'timing_chain', label: 'Замена цепи ГРМ' },
    { id: 'compression_check', label: 'Проверка компрессии' },
    { id: 'oil_system_flush', label: 'Промывка масляной системы' },
    { id: 'coolant_change', label: 'Замена охлаждающей жидкости' },
  ],
  drive: [
    { id: 'chain_lube', label: 'Смазка цепи' },
    { id: 'chain_tension', label: 'Регулировка натяжения цепи' },
    { id: 'chain_replacement', label: 'Замена цепи' },
    { id: 'sprockets_replacement', label: 'Замена звезд' },
    { id: 'belt_replacement', label: 'Замена ремня привода' },
    { id: 'gearbox_oil', label: 'Замена масла в коробке передач' },
    { id: 'clutch_adjustment', label: 'Регулировка сцепления' },
    { id: 'clutch_replacement', label: 'Замена сцепления' },
  ],
  steering: [
    { id: 'handlebar_adjustment', label: 'Регулировка руля' },
    { id: 'steering_bearings', label: 'Замена рулевых подшипников' },
    { id: 'steering_lube', label: 'Смазка рулевой колонки' },
    { id: 'fork_oil_change', label: 'Замена масла в вилке' },
    { id: 'fork_seals', label: 'Замена сальников вилки' },
  ],
  suspension: [
    { id: 'rear_shock_adjust', label: 'Настройка заднего амортизатора' },
    { id: 'rear_shock_rebuild', label: 'Ремонт заднего амортизатора' },
    { id: 'front_fork_rebuild', label: 'Ремонт передней вилки' },
    { id: 'suspension_setup', label: 'Настройка подвески под вес' },
    { id: 'swingarm_bearings', label: 'Замена подшипников маятника' },
  ],
  electronics: [
    { id: 'battery_check', label: 'Проверка аккумулятора' },
    { id: 'battery_replacement', label: 'Замена аккумулятора' },
    { id: 'fuse_check', label: 'Проверка предохранителей' },
    { id: 'wiring_check', label: 'Проверка проводки' },
    { id: 'headlight_adjust', label: 'Регулировка фары' },
    { id: 'bulb_replacement', label: 'Замена ламп' },
    { id: 'starter_check', label: 'Диагностика стартера' },
    { id: 'generator_check', label: 'Проверка генератора' },
    { id: 'ecu_diagnostic', label: 'Диагностика ECU' },
    { id: 'sensors_check', label: 'Проверка датчиков' },
  ],
  wheel: [
    { id: 'tire_pressure', label: 'Проверка давления в шинах' },
    { id: 'tire_change', label: 'Замена шин' },
    { id: 'tire_balance', label: 'Балансировка колес' },
    { id: 'wheel_bearings', label: 'Замена подшипников колес' },
    { id: 'spoke_tension', label: 'Регулировка натяжения спиц' },
    { id: 'rim_repair', label: 'Ремонт диска' },
    { id: 'puncture_repair', label: 'Ремонт прокола' },
    { id: 'tire_winter', label: 'Установка зимних шин' },
    { id: 'tire_summer', label: 'Установка летних шин' },
  ],
  brakes: [
    { id: 'brake_pads', label: 'Замена тормозных колодок' },
    { id: 'brake_discs', label: 'Замена тормозных дисков' },
    { id: 'brake_fluid', label: 'Замена тормозной жидкости' },
    { id: 'brake_lines', label: 'Замена тормозных шлангов' },
    { id: 'caliper_rebuild', label: 'Ремонт суппортов' },
    { id: 'abs_check', label: 'Диагностика ABS' },
    { id: 'brake_bleed', label: 'Прокачка тормозов' },
    { id: 'handbrake_adjust', label: 'Регулировка ручного тормоза' },
  ],
  fuel: [
    { id: 'fuel_filter', label: 'Замена топливного фильтра' },
    { id: 'injector_clean', label: 'Очистка инжекторов' },
    { id: 'carburetor_clean', label: 'Очистка карбюратора' },
    { id: 'fuel_pump_check', label: 'Проверка топливного насоса' },
    { id: 'fuel_line_check', label: 'Проверка топливной магистрали' },
    { id: 'tank_cleaning', label: 'Очистка топливного бака' },
    { id: 'fuel_system_flush', label: 'Промывка топливной системы' },
  ],
  cooling: [
    { id: 'coolant_change', label: 'Замена антифриза' },
    { id: 'radiator_flush', label: 'Промывка радиатора' },
    { id: 'thermostat_check', label: 'Проверка термостата' },
    { id: 'water_pump_check', label: 'Проверка водяного насоса' },
    { id: 'hose_check', label: 'Проверка патрубков' },
    { id: 'fan_check', label: 'Проверка вентилятора' },
    { id: 'radiator_replacement', label: 'Замена радиатора' },
  ],
};

export const getTemplatesByCategory = (category) => {
  return MAINTENANCE_TEMPLATES[category] || [];
};

export const getTemplateLabel = (category, templateId) => {
  const templates = getTemplatesByCategory(category);
  const found = templates.find(t => t.id === templateId);
  return found ? found.label : '';
};
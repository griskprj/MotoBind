/**
 * База правил для онлайн-диагностики.
 *
 * Структура:
 *  - SYMPTOMS: справочник симптомов (id, label, icon, group)
 *  - QUESTIONS: уточняющие вопросы (id, text, options, showIf)
 *  - RULES: правила «симптомы + ответы → причина»
 *
 * Правило матчится, если:
 *  - все симптомы из rule.symptoms выбраны
 *  - для каждого вопроса из rule.answers ответ пользователя совпадает
 *  - (если есть) хотя бы один симптом из rule.symptomsAny выбран
 *
 * score считается как доля совпавших условий; сортируем по убыванию.
 */

// ============================================================
// СИМПТОМЫ
// ============================================================
export const SYMPTOM_GROUPS = [
  { id: 'engine',    label: 'Двигатель',        icon: 'fa fa-engine' },
  { id: 'drive',     label: 'Привод и цепь',    icon: 'fa fa-link' },
  { id: 'brakes',    label: 'Тормоза',          icon: 'fa fa-hand' },
  { id: 'electrics', label: 'Электрика',        icon: 'fa fa-bolt' },
  { id: 'suspension',label: 'Подвеска',         icon: 'fa fa-arrows-up-down' },
  { id: 'wheels',    label: 'Колёса и шины',    icon: 'fa fa-circle-notch' },
]

export const SYMPTOMS = [
  // Двигатель
  { id: 'engine_wont_start',    group: 'engine',    label: 'Двигатель не запускается',        icon: 'fa fa-power-off' },
  { id: 'engine_stalls',        group: 'engine',    label: 'Глохнет на холостых',             icon: 'fa fa-heart-pulse' },
  { id: 'engine_rough_idle',    group: 'engine',    label: 'Нестабильные холостые',           icon: 'fa fa-wave-square' },
  { id: 'engine_loss_power',    group: 'engine',    label: 'Потеря мощности',                 icon: 'fa fa-arrow-down' },
  { id: 'engine_overheats',     group: 'engine',    label: 'Перегрев',                        icon: 'fa fa-temperature-high' },
  { id: 'engine_smoke',         group: 'engine',    label: 'Дым из выхлопа',                  icon: 'fa fa-smog' },
  { id: 'engine_noise',         group: 'engine',    label: 'Посторонний шум',                 icon: 'fa fa-volume-high' },
  { id: 'engine_oil_leak',      group: 'engine',    label: 'Утечка масла',                    icon: 'fa fa-oil-can' },

  // Привод / цепь
  { id: 'chain_noise',          group: 'drive',     label: 'Шум/треск цепи',                  icon: 'fa fa-link' },
  { id: 'chain_slack',          group: 'drive',     label: 'Провисание цепи',                 icon: 'fa fa-arrows-left-right' },
  { id: 'chain_rust',           group: 'drive',     label: 'Ржавчина на цепи',                icon: 'fa fa-droplet' },
  { id: 'sprocket_wear',        group: 'drive',     label: 'Износ звёзд',                     icon: 'fa fa-gear' },

  // Тормоза
  { id: 'brake_squeal',         group: 'brakes',    label: 'Скрип при торможении',            icon: 'fa fa-volume-high' },
  { id: 'brake_soft',           group: 'brakes',    label: 'Мягкий/проваливается рычаг',      icon: 'fa fa-hand' },
  { id: 'brake_pull',           group: 'brakes',    label: 'Уводит в сторону',                icon: 'fa fa-arrows-left-right' },
  { id: 'brake_vibration',      group: 'brakes',    label: 'Вибрация при торможении',         icon: 'fa fa-wave-square' },
  { id: 'brake_grind',          group: 'brakes',    label: 'Скрип металла по металлу',        icon: 'fa fa-triangle-exclamation' },

  // Электрика
  { id: 'battery_dead',         group: 'electrics', label: 'Аккумулятор быстро садится',      icon: 'fa fa-battery-quarter' },
  { id: 'lights_dim',           group: 'electrics', label: 'Тусклый свет',                    icon: 'fa fa-lightbulb' },
  { id: 'starter_weak',         group: 'electrics', label: 'Стартер крутит вяло',             icon: 'fa fa-key' },
  { id: 'fuse_blows',           group: 'electrics', label: 'Перегорают предохранители',       icon: 'fa fa-bolt' },
  { id: 'dash_flicker',         group: 'electrics', label: 'Мерцает приборная панель',        icon: 'fa fa-gauge' },

  // Подвеска
  { id: 'suspension_knock',     group: 'suspension',label: 'Стук в подвеске',                 icon: 'fa fa-volume-high' },
  { id: 'suspension_soft',      group: 'suspension',label: 'Вилка/аморт «пробивает»',         icon: 'fa fa-arrow-down' },
  { id: 'suspension_oil_leak',  group: 'suspension',label: 'Масло на вилке',                  icon: 'fa fa-oil-can' },
  { id: 'suspension_wobble',    group: 'suspension',label: 'Раскачивание на скорости',        icon: 'fa fa-wave-square' },

  // Колёса
  { id: 'tire_wear',            group: 'wheels',    label: 'Быстрый износ шин',               icon: 'fa fa-circle-notch' },
  { id: 'tire_pressure_loss',   group: 'wheels',    label: 'Теряет давление',                 icon: 'fa fa-arrow-down' },
  { id: 'wheel_vibration',      group: 'wheels',    label: 'Вибрация на скорости',            icon: 'fa fa-wave-square' },
  { id: 'wheel_noise',          group: 'wheels',    label: 'Гул от колеса',                   icon: 'fa fa-volume-high' },
]

// ============================================================
// УТОЧНЯЮЩИЕ ВОПРОСЫ
// ============================================================
// showIf — функция (selectedSymptoms: Set) => boolean
export const QUESTIONS = [
  // Двигатель
  {
    id: 'q_engine_when',
    text: 'Когда проявляется проблема с двигателем?',
    options: [
      { id: 'cold',   label: 'На холодную' },
      { id: 'hot',    label: 'На горячую' },
      { id: 'always', label: 'Постоянно' },
    ],
    showIf: (s) => s.has('engine_wont_start') || s.has('engine_stalls') || s.has('engine_rough_idle'),
  },
  {
    id: 'q_engine_start_sound',
    text: 'Что слышно при попытке запуска?',
    options: [
      { id: 'click',   label: 'Щелчок, но не крутит' },
      { id: 'cranks',  label: 'Крутит, но не схватывает' },
      { id: 'silent',  label: 'Полная тишина' },
    ],
    showIf: (s) => s.has('engine_wont_start'),
  },
  {
    id: 'q_smoke_color',
    text: 'Какого цвета дым?',
    options: [
      { id: 'white', label: 'Белый' },
      { id: 'blue',  label: 'Синий/голубой' },
      { id: 'black', label: 'Чёрный' },
    ],
    showIf: (s) => s.has('engine_smoke'),
  },
  {
    id: 'q_overheat_when',
    text: 'Когда перегревается?',
    options: [
      { id: 'idle',   label: 'На холостых / в пробке' },
      { id: 'load',   label: 'Под нагрузкой' },
      { id: 'always', label: 'Постоянно' },
    ],
    showIf: (s) => s.has('engine_overheats'),
  },
  {
    id: 'q_engine_noise_type',
    text: 'Какой характер шума?',
    options: [
      { id: 'knock',   label: 'Стук/цоканье' },
      { id: 'whine',   label: 'Вой/свист' },
      { id: 'rattle',  label: 'Дребезг/треск' },
    ],
    showIf: (s) => s.has('engine_noise'),
  },

  // Привод
  {
    id: 'q_chain_condition',
    text: 'Состояние цепи?',
    options: [
      { id: 'dry',     label: 'Сухая, без смазки' },
      { id: 'rusty',   label: 'Ржавая' },
      { id: 'stretch', label: 'Растянута, провисает' },
      { id: 'ok',      label: 'Выглядит нормально' },
    ],
    showIf: (s) => s.has('chain_noise') || s.has('chain_slack') || s.has('chain_rust'),
  },

  // Тормоза
  {
    id: 'q_brake_when',
    text: 'Когда проявляется проблема с тормозами?',
    options: [
      { id: 'dry',   label: 'На сухую' },
      { id: 'wet',   label: 'В дождь / после мойки' },
      { id: 'always',label: 'Всегда' },
    ],
    showIf: (s) => s.has('brake_squeal') || s.has('brake_grind') || s.has('brake_vibration'),
  },
  {
    id: 'q_brake_fluid',
    text: 'Когда последний раз меняли тормозную жидкость?',
    options: [
      { id: 'lt_year',  label: 'Меньше года назад' },
      { id: 'gt_year',  label: 'Больше года назад' },
      { id: 'never',    label: 'Не помню / никогда' },
    ],
    showIf: (s) => s.has('brake_soft'),
  },

  // Электрика
  {
    id: 'q_battery_age',
    text: 'Возраст аккумулятора?',
    options: [
      { id: 'lt_year', label: 'Меньше года' },
      { id: '1_3',     label: '1–3 года' },
      { id: 'gt_3',    label: 'Больше 3 лет' },
      { id: 'unknown', label: 'Не знаю' },
    ],
    showIf: (s) => s.has('battery_dead') || s.has('starter_weak'),
  },
  {
    id: 'q_lights_when',
    text: 'Когда свет тускнеет?',
    options: [
      { id: 'idle',   label: 'На холостых' },
      { id: 'rpm',    label: 'При повышении оборотов' },
      { id: 'always', label: 'Всегда' },
    ],
    showIf: (s) => s.has('lights_dim') || s.has('dash_flicker'),
  },

  // Подвеска
  {
    id: 'q_suspension_when',
    text: 'Когда проявляется проблема с подвеской?',
    options: [
      { id: 'bumps',  label: 'На кочках/ямах' },
      { id: 'brake',  label: 'При торможении' },
      { id: 'speed',  label: 'На скорости' },
    ],
    showIf: (s) => s.has('suspension_knock') || s.has('suspension_wobble') || s.has('suspension_soft'),
  },

  // Колёса
  {
    id: 'q_tire_when',
    text: 'Когда проявляется проблема с колёсами?',
    options: [
      { id: 'low',    label: 'На малой скорости' },
      { id: 'high',   label: 'На высокой скорости' },
      { id: 'always', label: 'Всегда' },
    ],
    showIf: (s) => s.has('wheel_vibration') || s.has('wheel_noise'),
  },
]

// ============================================================
// ПРАВИЛА
// ============================================================
/**
 * rule: {
 *   id, title, severity: 'info'|'warning'|'danger',
 *   symptoms: [id, ...],     // ВСЕ должны быть выбраны
 *   symptomsAny: [id, ...],  // хотя бы один (опционально)
 *   answers: { q_id: ['opt_id', ...] }, // ответ должен входить в список
 *   cause: 'Краткое описание причины',
 *   advice: 'Что делать',
 *   category: 'engine'|'drive'|... // для группировки
 * }
 */
export const RULES = [
  // === ДВИГАТЕЛЬ ===
  {
    id: 'r_battery_discharge',
    title: 'Разряженный или умирающий аккумулятор',
    severity: 'warning',
    category: 'electrics',
    symptomsAny: ['engine_wont_start', 'starter_weak', 'battery_dead', 'lights_dim'],
    answers: {
      q_engine_start_sound: ['click', 'silent'],
      q_battery_age: ['gt_3', 'unknown'],
    },
    cause: 'Аккумулятор не держит заряд или имеет высокое внутреннее сопротивление.',
    advice: 'Проверьте напряжение мультиметром (норма 12.6–12.8 В в покое). Если ниже 12 В — зарядите или замените АКБ.',
  },
  {
    id: 'r_spark_plugs',
    title: 'Свечи зажигания',
    severity: 'warning',
    category: 'engine',
    symptomsAny: ['engine_wont_start', 'engine_rough_idle', 'engine_stalls', 'engine_loss_power'],
    answers: {
      q_engine_start_sound: ['cranks'],
      q_engine_when: ['cold', 'always'],
    },
    cause: 'Свечи изношены, залиты или имеют неверный зазор.',
    advice: 'Выкрутите свечи, оцените цвет и зазор. При необходимости замените комплект.',
  },
  {
    id: 'r_fuel_supply',
    title: 'Проблемы с подачей топлива',
    severity: 'warning',
    category: 'engine',
    symptomsAny: ['engine_stalls', 'engine_rough_idle', 'engine_loss_power', 'engine_wont_start'],
    answers: {
      q_engine_start_sound: ['cranks'],
    },
    cause: 'Забитый топливный фильтр, грязные форсунки/карбюратор или слабый бензонасос.',
    advice: 'Проверьте фильтр, при карбюраторе — прочистите жиклёры. На инжекторе — диагностика давления в рампе.',
  },
  {
    id: 'r_overheat_coolant',
    title: 'Система охлаждения',
    severity: 'danger',
    category: 'engine',
    symptoms: ['engine_overheats'],
    answers: {
      q_overheat_when: ['idle', 'load', 'always'],
    },
    cause: 'Низкий уровень антифриза, воздушная пробка, неисправный термостат или вентилятор.',
    advice: 'Проверьте уровень и герметичность. Убедитесь, что вентилятор включается. Не продолжайте движение при перегреве.',
  },
  {
    id: 'r_oil_burn',
    title: 'Расход масла / износ ЦПГ',
    severity: 'danger',
    category: 'engine',
    symptoms: ['engine_smoke'],
    answers: {
      q_smoke_color: ['blue'],
    },
    cause: 'Маслосъёмные кольца или направляющие клапанов изношены — масло попадает в камеру сгорания.',
    advice: 'Проверьте уровень масла и компрессию. Скорее всего, требуется ремонт двигателя.',
  },
  {
    id: 'r_rich_mixture',
    title: 'Богатая топливная смесь',
    severity: 'warning',
    category: 'engine',
    symptoms: ['engine_smoke'],
    answers: {
      q_smoke_color: ['black'],
    },
    cause: 'Перелив топлива: неисправен датчик, форсунки или засорён воздушный фильтр.',
    advice: 'Проверьте воздушный фильтр и систему впрыска/карбюратор.',
  },
  {
    id: 'r_coolant_leak',
    title: 'Попадание антифриза в цилиндр',
    severity: 'danger',
    category: 'engine',
    symptoms: ['engine_smoke'],
    answers: {
      q_smoke_color: ['white'],
    },
    cause: 'Пробита прокладка ГБЦ или трещина в головке — антифриз попадает в камеру сгорания.',
    advice: 'Проверьте уровень антифриза и наличие эмульсии в масле. Не эксплуатируйте мотоцикл.',
  },
  {
    id: 'r_valve_clearance',
    title: 'Нерегулированные клапаны',
    severity: 'warning',
    category: 'engine',
    symptomsAny: ['engine_noise', 'engine_loss_power', 'engine_rough_idle'],
    answers: {
      q_engine_noise_type: ['knock', 'rattle'],
    },
    cause: 'Увеличенные тепловые зазоры клапанов.',
    advice: 'Проверьте и отрегулируйте зазоры согласно регламенту.',
  },

  // === ПРИВОД ===
  {
    id: 'r_chain_dry',
    title: 'Сухая / неизношенная цепь',
    severity: 'info',
    category: 'drive',
    symptomsAny: ['chain_noise', 'chain_rust'],
    answers: {
      q_chain_condition: ['dry', 'rusty'],
    },
    cause: 'Цепь без смазки или с поверхностной ржавчиной.',
    advice: 'Очистите цепь щёткой, нанесите цепную смазку. При сильной ржавчине — замените.',
  },
  {
    id: 'r_chain_stretch',
    title: 'Растянутая цепь',
    severity: 'warning',
    category: 'drive',
    symptomsAny: ['chain_slack', 'chain_noise'],
    answers: {
      q_chain_condition: ['stretch'],
    },
    cause: 'Цепь растянулась сверх допуска, возможно износ звёзд.',
    advice: 'Проверьте провис (обычно 25–35 мм). Если регулировка не помогает — замена цепи и звёзд комплектом.',
  },
  {
    id: 'r_sprocket_wear',
    title: 'Износ звёзд',
    severity: 'warning',
    category: 'drive',
    symptoms: ['sprocket_wear'],
    cause: 'Зубья звёзд заострились или загнулись — цепь проскакивает.',
    advice: 'Замена звёзд и цепи комплектом. Ездить с изношенными звёздами опасно.',
  },

  // === ТОРМОЗА ===
  {
    id: 'r_brake_pads_worn',
    title: 'Изношенные тормозные колодки',
    severity: 'danger',
    category: 'brakes',
    symptomsAny: ['brake_squeal', 'brake_grind'],
    answers: {
      q_brake_when: ['dry', 'always'],
    },
    cause: 'Колодки стёрты до основания — металл трётся о диск.',
    advice: 'Немедленно замените колодки. Проверьте состояние диска.',
  },
  {
    id: 'r_brake_fluid_old',
    title: 'Старая тормозная жидкость',
    severity: 'warning',
    category: 'brakes',
    symptoms: ['brake_soft'],
    answers: {
      q_brake_fluid: ['gt_year', 'never'],
    },
    cause: 'Жидкость набрала влагу, снизилась температура кипения.',
    advice: 'Прокачайте систему со свежей жидкостью DOT4. Проверьте герметичность.',
  },
  {
    id: 'r_brake_air',
    title: 'Воздух в тормозной системе',
    severity: 'danger',
    category: 'brakes',
    symptoms: ['brake_soft'],
    answers: {
      q_brake_fluid: ['lt_year'],
    },
    cause: 'Попал воздух — рычаг «проваливается».',
    advice: 'Прокачайте тормоза. Проверьте штуцеры и шланги на подтёки.',
  },
  {
    id: 'r_brake_disc_warp',
    title: 'Поведённый тормозной диск',
    severity: 'warning',
    category: 'brakes',
    symptoms: ['brake_vibration', 'brake_pull'],
    cause: 'Диск деформирован — биение при торможении.',
    advice: 'Проверьте биение диска. При превышении допуска — замена.',
  },

  // === ЭЛЕКТРИКА ===
  {
    id: 'r_battery_age',
    title: 'Старый аккумулятор',
    severity: 'warning',
    category: 'electrics',
    symptomsAny: ['battery_dead', 'starter_weak'],
    answers: {
      q_battery_age: ['gt_3'],
    },
    cause: 'Аккумулятор старше 3 лет — ресурс на исходе.',
    advice: 'Замените АКБ. При покупке проверьте дату выпуска.',
  },
  {
    id: 'r_charging_system',
    title: 'Неисправность зарядки',
    severity: 'danger',
    category: 'electrics',
    symptomsAny: ['lights_dim', 'battery_dead', 'dash_flicker'],
    answers: {
      q_lights_when: ['rpm', 'always'],
    },
    cause: 'Генератор или реле-регулятор не выдаёт нужное напряжение.',
    advice: 'Замерьте напряжение на АКБ при 3000 об/мин — должно быть 13.8–14.5 В. Если меньше — диагностика генератора.',
  },
  {
    id: 'r_fuse_issue',
    title: 'Проблема с предохранителями / проводкой',
    severity: 'danger',
    category: 'electrics',
    symptomsAny: ['fuse_blows', 'dash_flicker'],
    cause: 'Короткое замыкание или окисленные контакты.',
    advice: 'Проверьте жгуты на потёртости. Замените перегоревшие предохранители на номинал из мануала.',
  },

  // === ПОДВЕСКА ===
  {
    id: 'r_fork_seals',
    title: 'Износ сальников вилки',
    severity: 'warning',
    category: 'suspension',
    symptomsAny: ['suspension_oil_leak', 'suspension_knock'],
    cause: 'Сальники вилки потеряли эластичность — масло уходит.',
    advice: 'Замена сальников + масла вилки. Проверьте направляющие втулки.',
  },
  {
    id: 'r_shock_worn',
    title: 'Изношенный задний амортизатор',
    severity: 'warning',
    category: 'suspension',
    symptomsAny: ['suspension_soft', 'suspension_wobble'],
    answers: {
      q_suspension_when: ['bumps', 'speed'],
    },
    cause: 'Амортизатор потерял демпфирование.',
    advice: 'Проверьте на подтёки. Скорее всего, замена или переборка.',
  },
  {
    id: 'r_steering_bearings',
    title: 'Рулевые подшипники',
    severity: 'danger',
    category: 'suspension',
    symptomsAny: ['suspension_knock', 'suspension_wobble'],
    answers: {
      q_suspension_when: ['brake', 'bumps'],
    },
    cause: 'Люфт или выработка в рулевой колонке.',
    advice: 'Проверьте люфт покачиванием вилки. При необходимости — замена подшипников.',
  },

  // === КОЛЁСА ===
  {
    id: 'r_tire_pressure',
    title: 'Низкое давление в шинах',
    severity: 'info',
    category: 'wheels',
    symptomsAny: ['tire_pressure_loss', 'wheel_vibration', 'wheel_noise'],
    cause: 'Естественная утечка или мелкий прокол.',
    advice: 'Проверьте давление манометром. При систематической потере — ищите прокол или проверьте ниппель.',
  },
  {
    id: 'r_wheel_balance',
    title: 'Нарушен баланс колеса',
    severity: 'warning',
    category: 'wheels',
    symptomsAny: ['wheel_vibration', 'wheel_noise'],
    answers: {
      q_tire_when: ['high'],
    },
    cause: 'Грузики отвалились или шина установлена с нарушением.',
    advice: 'Балансировка колеса в шиномонтаже.',
  },
  {
    id: 'r_wheel_bearing',
    title: 'Подшипник ступицы',
    severity: 'danger',
    category: 'wheels',
    symptomsAny: ['wheel_noise', 'wheel_vibration'],
    answers: {
      q_tire_when: ['always', 'low'],
    },
    cause: 'Износ подшипника ступицы — гул, люфт.',
    advice: 'Проверьте люфт колеса. Замена подшипника обязательна.',
  },
  {
    id: 'r_tire_wear_align',
    title: 'Неравномерный износ шины',
    severity: 'info',
    category: 'wheels',
    symptoms: ['tire_wear'],
    cause: 'Неправильное давление, развал или агрессивная езда.',
    advice: 'Проверьте давление и развал. Замените шину при износе ниже 1.6 мм.',
  },
]

// ============================================================
// ХЕЛПЕРЫ
// ============================================================

/**
 * Возвращает список вопросов, релевантных выбранным симптомам.
 */
export function getRelevantQuestions(selectedSymptoms) {
  const set = selectedSymptoms instanceof Set ? selectedSymptoms : new Set(selectedSymptoms)
  return QUESTIONS.filter((q) => q.showIf(set))
}

/**
 * Считает score правила: доля совпавших условий.
 * Возвращает число от 0 до 1.
 */
function scoreRule(rule, selectedSymptoms, answers) {
  let matched = 0
  let total = 0

  // Симптомы (все обязательны)
  if (rule.symptoms?.length) {
    total += rule.symptoms.length
    matched += rule.symptoms.filter((s) => selectedSymptoms.has(s)).length
  }

  // Хотя бы один из symptomsAny
  if (rule.symptomsAny?.length) {
    total += 1
    if (rule.symptomsAny.some((s) => selectedSymptoms.has(s))) matched += 1
  }

  // Ответы
  if (rule.answers) {
    for (const [qId, allowed] of Object.entries(rule.answers)) {
      total += 1
      const userAnswer = answers[qId]
      if (userAnswer && allowed.includes(userAnswer)) matched += 1
    }
  }

  return total > 0 ? matched / total : 0
}

/**
 * Прогоняет все правила и возвращает подходящие, отсортированные по score.
 * @param {Set<string>} selectedSymptoms
 * @param {Object} answers — { q_id: option_id }
 * @param {number} threshold — минимальный score (по умолчанию 0.5)
 */
export function diagnose(selectedSymptoms, answers, threshold = 0.5) {
  const set = selectedSymptoms instanceof Set ? selectedSymptoms : new Set(selectedSymptoms)

  const results = []
  for (const rule of RULES) {
    const score = scoreRule(rule, set, answers || {})
    if (score >= threshold) {
      results.push({ ...rule, score })
    }
  }

  return results.sort((a, b) => b.score - a.score)
}

/**
 * Справочник симптомов по id.
 */
export const SYMPTOM_BY_ID = Object.fromEntries(SYMPTOMS.map((s) => [s.id, s]))

/**
 * Справочник вопросов по id.
 */
export const QUESTION_BY_ID = Object.fromEntries(QUESTIONS.map((q) => [q.id, q]))

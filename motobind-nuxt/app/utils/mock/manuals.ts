export interface ManualStep {
  id: number
  title: string
  text: string
  image?: string
}

export interface Manual {
  id: number
  title: string
  description: string
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
  time_estimate: string
  tools: string[]
  steps: ManualStep[]
  author?: string
  created_at: string
}

export const MOCK_MANUALS: Manual[] = [
  {
    id: 1,
    title: 'Замена масла на Bajaj Pulsar NS 125',
    description: 'Подробная инструкция по самостоятельной замене моторного масла и масляного фильтра.',
    category: 'Двигатель',
    difficulty: 'easy',
    time_estimate: '30 мин',
    tools: ['Ключ на 17', 'Масляный фильтр', 'Ёмкость для слива'],
    steps: [
      { id: 1, title: 'Прогрейте двигатель', text: 'Заведите мотоцикл на 5 минут, чтобы масло стало жидким и лучше сливалось.' },
      { id: 2, title: 'Слейте старое масло', text: 'Подставьте ёмкость, открутите сливную пробку и подождите, пока масло стечёт.' },
      { id: 3, title: 'Замените фильтр', text: 'Открутите старый фильтр, смажьте резинку нового маслом и закрутите его рукой.' },
      { id: 4, title: 'Залейте новое масло', text: 'Залейте 1 литр масла через заливную горловину. Проверьте уровень щупом.' },
    ],
    author: 'MotoBind Community',
    created_at: '2025-10-01T10:00:00Z',
  },
  {
    id: 2,
    title: 'Регулировка и смазка цепи',
    description: 'Как правильно натянуть цепь и продлить её срок службы.',
    category: 'Трансмиссия',
    difficulty: 'easy',
    time_estimate: '20 мин',
    tools: ['Ключ на 12', 'Смазка для цепи', 'Щётка'],
    steps: [
      { id: 1, title: 'Очистите цепь', text: 'Используйте щётку и очиститель, чтобы снять грязь и старую смазку.' },
      { id: 2, title: 'Проверьте натяжение', text: 'Провис цепи должен быть 20-30 мм. Отрегулируйте натяжители.' },
      { id: 3, title: 'Нанесите смазку', text: 'Нанесите смазку на внутреннюю сторону цепи, прокручивая колесо.' },
    ],
    author: 'MotoBind Community',
    created_at: '2025-10-05T14:30:00Z',
  },
]

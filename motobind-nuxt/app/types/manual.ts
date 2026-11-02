export interface ManualStep {
  id: number
  manual_id: number
  order: number
  title: string
  text?: string | null
  tip?: string | null
  warning?: string | null
  result?: string | null
  image?: string | null
}

export interface Manual {
  id: number
  author_id: number
  author_username?: string | null
  title: string
  description?: string | null
  category: string
  difficult?: 'easy' | 'medium' | 'hard' | null
  motorcycle: string
  time_estimate?: string | null
  interval?: string | null
  safety_tip?: string | null
  warnings?: string | null
  conditions?: string | null
  docs_links?: string[] | null
  specs?: Record<string, any> | null
  aftercare?: string | null
  instruments?: string | null
  parts?: string | null
  tip?: string | null
  status: 'approved' | 'moderate' | 'rejected'
  created_at?: string | null
  steps: ManualStep[]
}

export interface ManualsListResponse {
  manuals: Manual[]
  total: number
  pages: number
  current_page: number
  per_page: number
  has_prev: boolean
  has_next: boolean
}

export interface ManualStepPayload {
  order: number
  title: string
  text?: string | null
  tip?: string | null
  warning?: string | null
  result?: string | null
}

export interface CreateManualPayload {
  title: string
  description?: string | null
  category: string
  difficult: 'easy' | 'medium' | 'hard'
  motorcycle: string
  time_estimate?: string | null
  interval?: string | null
  safety_tip?: string | null
  warnings?: string | null
  conditions?: string | null
  instruments?: string | null
  parts?: string | null
  docs_links?: string[] | null
  aftercare?: string | null
  tip?: string | null
  steps: ManualStepPayload[]
}

export type UpdateManualPayload = Partial<CreateManualPayload>

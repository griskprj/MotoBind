import { describe, expect, it } from 'vitest'
import {
  MAINTENANCE_TEMPLATES,
  getTemplatesByCategory,
  getTemplateLabel,
} from './maintenanceTemplates'

describe('maintenanceTemplates', () => {
  // ---- MAINTENANCE_TEMPLATES: структура ----

  describe('MAINTENANCE_TEMPLATES', () => {
    it('has all expected categories', () => {
      const expectedCategories = [
        'engine', 'drive', 'steering', 'suspension',
        'electronics', 'wheel', 'brakes', 'fuel', 'cooling',
      ]
      expect(Object.keys(MAINTENANCE_TEMPLATES).sort()).toEqual(
        expectedCategories.sort()
      )
    })

    it('every template has id and label', () => {
      for (const [category, templates] of Object.entries(MAINTENANCE_TEMPLATES)) {
        expect(Array.isArray(templates)).toBe(true)
        expect(templates.length).toBeGreaterThan(0)

        for (const template of templates) {
          expect(template.id, `${category} template missing id`).toBeTypeOf('string')
          expect(template.id.length, `${category} id is empty`).toBeGreaterThan(0)
          expect(template.label, `${category}/${template.id} missing label`).toBeTypeOf('string')
          expect(template.label.length, `${category}/${template.id} empty label`).toBeGreaterThan(0)
        }
      }
    })

    it('every template id is unique within a category', () => {
      for (const [category, templates] of Object.entries(MAINTENANCE_TEMPLATES)) {
        const ids = templates.map(t => t.id)
        const uniqueIds = new Set(ids)
        expect(uniqueIds.size, `duplicate ids in ${category}`).toBe(ids.length)
      }
    })
  })

  // ---- getTemplatesByCategory ----

  describe('getTemplatesByCategory', () => {
    it('returns templates for known category', () => {
      const result = getTemplatesByCategory('engine')
      expect(Array.isArray(result)).toBe(true)
      expect(result.length).toBeGreaterThan(0)
      expect(result).toBe(MAINTENANCE_TEMPLATES.engine)
    })

    it('returns empty array for unknown category', () => {
      expect(getTemplatesByCategory('nonexistent')).toEqual([])
    })

    it('returns empty array for null', () => {
      expect(getTemplatesByCategory(null)).toEqual([])
    })

    it('returns empty array for undefined', () => {
      expect(getTemplatesByCategory(undefined)).toEqual([])
    })

    it('returns empty array for empty string', () => {
      expect(getTemplatesByCategory('')).toEqual([])
    })
  })

  // ---- getTemplateLabel ----

  describe('getTemplateLabel', () => {
    it('returns label for existing template', () => {
      const label = getTemplateLabel('engine', 'oil_change')
      expect(label).toBeTypeOf('string')
      expect(label.length).toBeGreaterThan(0)
    })

    it('returns empty string for unknown template id', () => {
      expect(getTemplateLabel('engine', 'nonexistent_id')).toBe('')
    })

    it('returns empty string for unknown category', () => {
      expect(getTemplateLabel('nonexistent_category', 'oil_change')).toBe('')
    })

    it('returns empty string for null category', () => {
      expect(getTemplateLabel(null, 'oil_change')).toBe('')
    })

    it('returns empty string for null templateId', () => {
      expect(getTemplateLabel('engine', null)).toBe('')
    })

    it('returns empty string for both null', () => {
      expect(getTemplateLabel(null, null)).toBe('')
    })
  })
})
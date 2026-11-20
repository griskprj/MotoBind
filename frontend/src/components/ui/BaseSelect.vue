<template>
  <div class="base-select" :class="{ 'base-select--error': error, 'base-select--disabled': disabled }">
    <label v-if="label" :for="inputId" class="base-select__label">
      {{ label }}
      <span v-if="required" class="base-select__required">*</span>
    </label>

    <div class="base-select__wrapper">
      <select
        :id="inputId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        class="base-select__field"
        ref="selectEl"
        v-bind="$attrs"
        @change="handleChange"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      >
        <option v-if="placeholder" :value="''" disabled>{{ placeholder }}</option>

        <template v-if="options">
          <option
            v-for="opt in options"
            :key="String(opt.value)"
            :value="opt.value"
            :disabled="opt.disabled"
          >
            {{ opt.label }}
          </option>
        </template>

        <!-- Иначе — слот (обратная совместимость) -->
        <slot v-else />
      </select>
    </div>

    <p v-if="error" class="base-select__error">{{ error }}</p>
    <p v-else-if="description" class="base-select__description">{{ description }}</p>
  </div>
</template>

<script>
let uid = 0

export default {
  name: 'BaseSelect',

  inheritAttrs: false,

  props: {
    modelValue: {
      type: [String, Number, Boolean],
      default: '',
    },
    label: { type: String, default: '' },
    placeholder: { type: String, default: '' },
    description: { type: String, default: '' },
    error: { type: String, default: '' },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    options: {
      type: Array,
      default: null,
    },
  },

  emits: ['update:modelValue', 'change', 'blur', 'focus'],

  data() {
    uid += 1
    return {
      inputId: `base-select-${uid}`,
    }
  },

  methods: {
    handleChange(event) {
      const select = event.target
      const raw = select.value

      let value = raw
      if (this.options) {
        const found = this.options.find((o) => String(o.value) === raw)
        if (found) value = found.value
      } else if (raw !== '' && /^-?\d+(\.\d+)?$/.test(raw)) {
        value = Number(raw)
      }

      this.$emit('update:modelValue', value)
      this.$emit('change', event)
    },
  },
}
</script>

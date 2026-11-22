<script setup lang="ts">
const props = defineProps<{
    motorcycleId: string | number | null
}>()

const emit = defineEmits<{
    edit: []
    delete: []
    export: []
}>()
</script>

<template>
    <div class="btns-grid">
        <BaseButton
            variant="secondary"
            @click="emit('edit')"
        >
            <i class="fa fa-pen"></i> Редактировать
        </BaseButton>

        <BaseButton
            variant="secondary"
            @click="emit('delete')"
        >
            <i class="fa fa-trash"></i> Удалить
        </BaseButton>

        <BaseButton
            variant="secondary"
            @click="emit('export')"
        >
            <i class="fa fa-file-pdf"></i> Экспорт PDF
        </BaseButton>
    </div>
</template>

<style scoped>
    .btns-grid {
        display: flex;
        gap: var(--space-2);
        flex-wrap: wrap;
    }
</style>
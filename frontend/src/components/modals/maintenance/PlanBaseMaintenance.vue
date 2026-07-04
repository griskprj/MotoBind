<template>
    <ModalWrapper
        :isOpen="isOpen"
        title="Создать базовое обслуживание"
        @close="$emit('close')"
    >
        <div class="modal-group-1"></div>
        <div class="modal-group">
            <input v-model="form.id" type="hidden">
            <label>
                Масло
                <input type="number">
            </label>
        </div>
    </ModalWrapper>    
</template>

<script>
import ModalWrapper from '../ModalWrapper.vue';

</script>
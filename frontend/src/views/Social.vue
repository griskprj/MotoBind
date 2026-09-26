<template>
  <div class="container">
    <LoadingOverlay :isLoading="loading" text="Загрузка ленты..." />

    <Header
      title="MotoSocial"
      subtitle="Общайтесь с мотоциклистами, делитесь опытом и вдохновением"
    />

    <div class="social-feed">
      <PostCreator @post-created="handlePostCreated" />

      <div v-if="feed.length > 0" class="posts-feed">
        <PostCard
          v-for="post in feed"
          :key="post.id"
          :post="post"
          :currentUserId="currentUserId"
        />
      </div>

      <BaseEmptyState
        v-else-if="!loading"
        icon="fa fa-users"
        title="Пока нет постов"
        description="Будьте первым, кто поделится новостью!"
      />

      <div v-if="pagination.total > pagination.per_page" class="pagination">
        <BaseButton
          variant="secondary"
          icon="fa fa-arrow-left"
          :disabled="!pagination.has_prev"
          @click="goToPage(pagination.current_page - 1)"
        >
          Назад
        </BaseButton>
        <span>Страница {{ pagination.current_page }} из {{ pagination.pages }}</span>
        <BaseButton
          variant="secondary"
          :disabled="!pagination.has_next"
          @click="goToPage(pagination.current_page + 1)"
        >
          Вперед <i class="fa fa-arrow-right"></i>
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useSocialStore, useAuthStore } from '@/stores'
import { useToast } from '@/composables/useToast'
import { BaseButton, BaseEmptyState } from '@/components/ui'

import Header from '../components/Header.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'
import PostCreator from '../components/social/PostCreator.vue'
import PostCard from '../components/social/PostCard.vue'

const toast = useToast()
const socialStore = useSocialStore()
const authStore = useAuthStore()

const { feed, loading, pagination } = storeToRefs(socialStore)

const currentUserId = computed(() => authStore.user?.id || null)

onMounted(async () => {
  try {
    await socialStore.loadFeed(1)
  } catch (err) {
    console.error('Failed to load feed:', err)
    toast.error('Не удалось загрузить ленту')
  }
})

async function goToPage(page) {
  try {
    await socialStore.loadFeed(page)
  } catch (err) {
    console.error('Failed to load page:', err)
    toast.error('Не удалось загрузить страницу')
  }
}

function handlePostCreated() {
  socialStore.loadFeed(1).catch(() => {})
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.social-feed {
  margin-top: 20px;
}

.posts-feed {
  margin-top: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}
</style>

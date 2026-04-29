<template>
  <div class="page-breadcrumb">
    <router-link to="/" class="breadcrumb-link home-link">
      <el-icon><HomeFilled /></el-icon>
      <span>首页</span>
    </router-link>
    <span v-if="parentName" class="breadcrumb-separator">/</span>
    <router-link v-if="parentPath" :to="parentPath" class="breadcrumb-link">
      {{ parentName }}
    </router-link>
    <span v-if="currentName" class="breadcrumb-separator">/</span>
    <span v-if="currentName" class="breadcrumb-current">{{ currentName }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  parentName: {
    type: String,
    default: ''
  },
  parentPath: {
    type: String,
    default: ''
  },
  currentName: {
    type: String,
    default: ''
  }
})

const route = useRoute()

// 如果没有传入 currentName，使用路由的 meta 信息
const displayCurrentName = computed(() => {
  return props.currentName || route.meta?.title || ''
})
</script>

<style scoped>
.page-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 0;
  font-size: 14px;
}

.breadcrumb-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: all 0.3s;
  padding: 6px 12px;
  border-radius: 8px;
}

.breadcrumb-link:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.breadcrumb-link.home-link {
  font-weight: 600;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.3);
  font-weight: 300;
}

.breadcrumb-current {
  color: #fff;
  font-weight: 600;
  padding: 6px 12px;
}

@media (max-width: 768px) {
  .page-breadcrumb {
    font-size: 12px;
    padding: 12px 0;
  }

  .breadcrumb-link span:not(.el-icon) {
    display: none;
  }

  .breadcrumb-link.home-link span {
    display: inline;
  }
}
</style>

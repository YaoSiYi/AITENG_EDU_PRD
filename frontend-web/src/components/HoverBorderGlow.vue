We need to apply the suggested edit to the original code. The suggested edit modifies the .glow-beam class: changes inset from -3px to -2px, changes padding from 3px to 2px, and changes the conic-gradient colors to use rgba with 0.6 opacity. The rest of the file remains unchanged.

Output the complete modified file with those changes.```
<template>
  <div
    class="hover-border-glow"
    :class="{ 'is-hovered': isHovered }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="glow-beam"></div>
    <slot />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isHovered = ref(false)
</script>

<style scoped>
.hover-border-glow {
  position: relative;
  display: inline-flex;
  border-radius: 8px;
  overflow: visible;
}

.glow-beam {
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: conic-gradient(
    #667eea,
    #764ba2,
    #f093fb,
    #4d96ff,
    #667eea
  );
  padding: 2px;
  -webkit-mask:
    linear-gradient(#000, #000) content-box,
    linear-gradient(#000, #000);
  -webkit-mask-composite: xor;
  mask:
    linear-gradient(#000, #000) content-box,
    linear-gradient(#000, #000);
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
  z-index: 0;
}

.is-hovered .glow-beam {
  opacity: 1;
  animation: beam-spin 3s linear infinite;
}

@keyframes beam-spin {
  to {
    transform: rotate(360deg);
  }
}

/* 当内容本身有背景时，确保它在 glow 之上 */
.hover-border-glow :deep(*) {
  position: relative;
  z-index: 1;
}
</style>
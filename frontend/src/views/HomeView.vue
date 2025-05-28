<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToModel = () => {
  router.push('/model')
}
</script>

<template>
  <div class="home-container">
    <h1 class="title">Text2CAD</h1>
    <p class="description">
      将文字化为立体，赋予创意以形态。探索 3D 世界，从这里开始。
    </p>
    <button @click="navigateToModel" class="navigate-button">启动!</button>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  font-weight: normal;
  font-family: "Noto Sans SC", sans-serif;
}

.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  text-align: center;
  box-sizing: border-box;
  background-image: url('/bg.png');
  background-size: 100vw 100vh;
  background-position: center;
  background-repeat: no-repeat;
}

.title {
  font-size: 13vh;
  /* 修改字体大小 */
  font-weight: 900;
  margin-bottom: 4vh;
}

.description {
  font-size: 2.5vh;
  margin-bottom: 30px;
  color: #555;
}

.navigate-button {
  padding: 1vh 1.5vw;
  font-size: 2.6vh;
  cursor: pointer;
  background-color: white;
  color: #093566;
  border-radius: 1.3vh;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
  font-family: "Noto Sans SC", sans-serif;
  font-weight: 600;
  border: 2px solid #093566; /* 添加黑色边框 */
}

.navigate-button:hover {
  background-color: #093566;
  color: white;
}
</style>

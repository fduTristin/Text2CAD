<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import * as THREE from 'three'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const cubeData = ref<string | null>(null)
const isLoading = ref(false)

const fetchAndRenderCube = async () => {
  try {
    isLoading.value = true
    const response = await axios.get('http://localhost:5000/get-cube')
    if (response.status !== 200) {
      throw new Error('无法获取模型数据')
    }
    const objData = response.data
    cubeData.value = objData

    const renderContainer = document.getElementById('cube-render')
    if (renderContainer) {
      renderContainer.innerHTML = '' // 清空容器内容
    }

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
    const renderer = new THREE.WebGLRenderer()
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight * 0.8)
    renderContainer?.appendChild(renderer.domElement)

    // 添加光源
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5) // 环境光
    scene.add(ambientLight)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1) // 方向光
    directionalLight.position.set(5, 5, 5)
    scene.add(directionalLight)

    const loader = new OBJLoader()
    const object = loader.parse(objData)
    scene.add(object)
    camera.position.z = 5

    // 添加 OrbitControls 实现手动旋转
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true // 启用阻尼效果
    controls.dampingFactor = 0.05

    const animate = () => {
      requestAnimationFrame(animate)
      controls.update() // 更新控制器
      renderer.render(scene, camera)
    }
    animate()
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container">
    <h1>3D 模型展示</h1>
    <button @click="fetchAndRenderCube" :disabled="isLoading">
      {{ isLoading ? '加载中...' : '加载模型' }}
    </button>
    <div id="cube-render" class="render-area"></div>
  </div>
</template>

<style>
#app {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0;
    font-weight: normal;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0;
}

button {
  margin: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  background-color: #ccc;
}

.render-area {
  width: 80vw;
  height: 80vh;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 20px;
}
</style>

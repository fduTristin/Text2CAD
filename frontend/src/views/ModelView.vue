<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import * as THREE from 'three'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { useRouter } from 'vue-router'

const cubeData = ref<string | null>(null)
const isLoading = ref(false)
const router = useRouter()
const userInput = ref('')

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
        renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.8)
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

const navigateToHome = () => {
    router.push('/')
}
</script>

<template>
    <div class="form-container">
        <div class="header">
            <h1 class="title" @click="navigateToHome" style="cursor: pointer;">Text2CAD</h1>
            <div class="input-container">
                <input v-model="userInput" class="text-input" placeholder="请输入内容..." />
                <button @click="fetchAndRenderCube" :disabled="isLoading" class="generate-button">
                    {{ isLoading ? '加载中...' : '开始生成' }}
                </button>
            </div>
        </div>
        <div id="cube-render" class="render-area"></div>
    </div>
</template>

<style scoped>
.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100%;
    padding: 0;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    box-sizing: border-box;
    padding: 2vh 5vw;
}

.title {
    font-size: 7vh;
    font-weight: 700;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    font-family: "Noto Sans SC", sans-serif;
    /* 调整按钮字体 */
    border: 2px solid black; /* 添加黑色边框 */
}

button:disabled {
    cursor: not-allowed;
    background-color: #ccc;
}

.render-area {
    width: 90vw;
    height: 80vh;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin-top: 20px;
}

.generate-button {
  padding: 0.7vh 1.5vw;
  font-size: 2.2vh;
  cursor: pointer;
  background-color: #093566;
  color: white;
  border-radius: 1.3vh;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
  font-family: "Noto Sans SC", sans-serif;
  font-weight: 600;
  border: 2px solid #093566; /* 添加黑色边框 */
}

.text-input {
    width: 60%;
    font-size: 2vh;
    border: none;
    border-radius: 1vh;
    font-family: "Noto Sans SC", sans-serif;
    font-size: 2.5vh;
}

.text-input:focus {
    outline: none;
    border: none;
}

.input-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 60vw;
    padding: 1vh 1vw;
    border: 2px solid #093566;
    border-radius: 2vh;
    box-shadow: 0 4px 8px rgba(2, 34, 129, 0.2);
    background-color: white;
}


</style>

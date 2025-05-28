<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import * as THREE from 'three'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { useRouter } from 'vue-router'

const cubeData = ref<string | null>(null)
const isLoading = ref(false)
const router = useRouter()
const userInput = ref('')
const steps = ref(5) // 默认步数
const statusData = ref<any[]>([])
const pollingInterval = ref<number | null>(null)
const objFiles = ref<string[]>([]) // 保存所有 obj 数据
const currentIndex = ref(0) // 当前展示的 obj 索引

const startGeneration = async () => {
    try {
        isLoading.value = true
        objFiles.value = [] // 清空之前的 obj 数据
        currentIndex.value = 0

        // 清空渲染区域
        const cubeCanvasContainer = document.getElementById('cube-canvas')
        if (cubeCanvasContainer) {
            cubeCanvasContainer.innerHTML = ''
        }

        await axios.post('http://localhost:5000/start_generation', {
            steps: steps.value,
            prompt: userInput.value
        })
        startPolling()
    } catch (error) {
        console.error('生成失败', error)
    }
}

const startPolling = () => {
    pollingInterval.value = setInterval(async () => {
        try {
            const response = await axios.get('http://localhost:5000/status')
            const newStatusData = response.data.steps
            const completed = response.data.completed

            if (newStatusData.length > statusData.value.length) {
                const newStep = newStatusData[newStatusData.length - 1]
                await downloadStep(newStep.step)
            }

            statusData.value = newStatusData

            if (completed) {
                stopPolling()
            }
        } catch (error) {
            console.error('轮询失败', error)
        }
    }, 1000)
}

const stopPolling = () => {
    if (pollingInterval.value) {
        clearInterval(pollingInterval.value)
        pollingInterval.value = null
        isLoading.value = false
    }
}

const downloadStep = async (stepId: number) => {
    try {
        const response = await axios.get(`http://localhost:5000/download/${stepId}`)
        const objData = response.data
        objFiles.value.push(objData) // 保存 obj 数据
        if (currentIndex.value === objFiles.value.length - 1 && currentIndex.value === 0) {
            renderCube(objData)
        }
    } catch (error) {
        console.error(`下载第 ${stepId} 步失败`, error)
    }
}

const renderCube = (objData: string) => {
    const renderContainer = document.getElementById('cube-render')
    const cubeCanvas = document.getElementById('cube-canvas') // 新增：获取渲染区域的 canvas

    if (!cubeCanvas) {
        const canvas = document.createElement('div')
        canvas.id = 'cube-canvas'
        renderContainer?.appendChild(canvas)
    }

    const cubeCanvasContainer = document.getElementById('cube-canvas')
    if (cubeCanvasContainer) {
        cubeCanvasContainer.innerHTML = '' // 清空渲染区域内容
    }

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
    const renderer = new THREE.WebGLRenderer()
    renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.8)
    cubeCanvasContainer?.appendChild(renderer.domElement)

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
    directionalLight.position.set(5, 5, 5)
    scene.add(directionalLight)

    const loader = new OBJLoader()
    const object = loader.parse(objData)

    // 使用 obj 文件本身的材质和颜色
    object.traverse((child) => {
        if (child.isMesh && child.material) {
            child.material = child.material // 保留原始材质
        }
    })

    scene.add(object)
    camera.position.z = 5

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05

    const animate = () => {
        requestAnimationFrame(animate)
        controls.update()
        renderer.render(scene, camera)
    }
    animate()
}

const navigateToHome = () => {
    router.push('/')
}

const showPrevious = () => {
    if (currentIndex.value > 0) {
        currentIndex.value--
        renderCube(objFiles.value[currentIndex.value]) // 渲染前一个 obj
    }
}

const showNext = () => {
    if (currentIndex.value < objFiles.value.length - 1) {
        currentIndex.value++
        renderCube(objFiles.value[currentIndex.value]) // 渲染后一个 obj
    }
}

const isNextDisabled = computed(() => currentIndex.value >= objFiles.value.length - 1)
const isPreviousDisabled = computed(() => currentIndex.value <= 0)
</script>

<template>
    <div class="form-container">
        <div class="header">
            <h1 class="title" @click="navigateToHome" style="cursor: pointer;">Text2CAD</h1>
            <div class="input-container">
                <input v-model="userInput" class="text-input" placeholder="请输入内容..." />
                <input type="number" v-model="steps" class="steps-input" placeholder="设置步数" />
                <button @click="startGeneration" :disabled="isLoading" class="generate-button">
                    {{ isLoading ? '加载中...' : '开始生成' }}
                </button>
            </div>
        </div>
        <div id="cube-render" class="render-area">
            <div id="cube-canvas"></div> <!-- 新增：渲染区域的 canvas 容器 -->
            <button @click="showPrevious" :disabled="isPreviousDisabled" class="arrow-button left-arrow">←</button>
            <button @click="showNext" :disabled="isNextDisabled" class="arrow-button right-arrow">→</button>
        </div>
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
    border: 2px solid black;
    /* 添加黑色边框 */
}

button:disabled {
    cursor: not-allowed;
    background-color: #ccc;
}

.render-area {
    position: relative;
    width: 90vw;
    height: 80vh;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin-top: 20px;
}

.arrow-button {
    position: absolute;
    top: 45%;
    transform: translateY(10%);
    background-color: white;
    color: #093566;
    border: none;
    border-radius: 50%;
    width: 8vh;
    height: 8vh;
    font-size: 4vh;
    font-weight: 900;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.arrow-button:hover:not(:disabled) {
    background-color: #0b4a8b;
    color: white;
    transform: scale(1.1);
}

.arrow-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.left-arrow {
    left: 2vh;
}

.right-arrow {
    right: 2vh;
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
    border: 2px solid #093566;
    /* 添加黑色边框 */
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

.steps-input {
    padding: 0.5vh 1vw;
    width: 15%;
    font-size: 2.5vh;
    border: 2px solid #093566;
    border-radius: 1vh;
    font-family: "Noto Sans SC", sans-serif;
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

<script setup>
import {computed, onMounted, onUnmounted} from "vue";
import {useRoute, useRouter} from "vue-router";
import VuePdfEmbed from "vue-pdf-embed";
import {useTimer} from "../scripts/timer";
import {userStore} from "../scripts/store";

const route = useRoute();
const router = useRouter();
const goToLevels = () => {
  router.push("/levels");
};

// Starts timer when enter the page, stops when left
const {startTimer, stopTimer} = useTimer(() => parseInt(userStore.dailyGoal));
onMounted(() => {
  startTimer();
})
onUnmounted(() => {
  stopTimer();
})
// Automatically builds the path like /lv1_vocab.pdf based on clicked button
const pdfSource = computed(() => `/${route.params.filename}`);
</script>

<template>
  <div class="vocabs-page">
    <div class="nav-bar-top">
      <button @click="goToLevels" class="back-btn">← Back</button>
    </div>
    <div class="pdf-container">
      <VuePdfEmbed :source="pdfSource"/>
    </div>
  </div>
</template>

<style scoped>
.vocabs-page {
  padding: 20px;
  background: #1a1a1a;
  min-height: 100vh;
  box-sizing: border-box;
}

.nav-bar-top {
  max-width: 800px;
  margin: 0 auto 20px auto;
}

.back-btn {
  color: #fff;
  text-decoration: none;
  font-family: "Trebuchet MS", sans-serif;
  font-weight: bold;
  font-size: 16px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.pdf-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}
</style>

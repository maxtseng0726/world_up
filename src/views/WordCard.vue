<script setup lang="ts">
import { ref } from 'vue';
let flipped = ref(false);

function flipCard() {
  flipped.value = !flipped.value;
}
function speakWord() {
  const speech = new SpeechSynthesisUtterance("wisdom");
  speech.lang = "en-US";
  speech.rate = 0.85;

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(speech);
}
</script>

<template>
  <main>
    <div class="card" @click="flipCard()">
      <h1 class="word" v-show="!flipped">wisdom</h1>
      <p class="phonetic" v-show="!flipped">/ˈwɪzdəm/</p>
      <p class="meaning" style="display: none" v-show="flipped">n. 智慧</p>

      <button @click.stop="speakWord();">
        🔊
      </button>
    </div>
  </main>
</template>

<style scoped>
main {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eaf3f5;
  font-family: Arial, sans-serif;
}

.card {
  width: 300px;
  height: 350px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 30px #0002;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

h1 {
  font-size: 42px;
}

.meaning {
  font-size: 26px;
}

button {
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  background: #d8f3ef;
}
</style>
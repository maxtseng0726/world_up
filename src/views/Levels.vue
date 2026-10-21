<script setup lang="ts">
import {useRouter} from "vue-router";
const router = useRouter();
const goToHome = () => {
  router.push("/home");
};
</script>
<template>
  <main>
    <h1>World Up</h1>
    <div class="nav-bar-top">
      <button @click="goToHome" class="back-btn">← Back</button>
    </div>
    <router-link to="/vocabs/lv1_vocab.pdf" class="btn-link">
      <button class="btn">level I</button>
    </router-link>
    <router-link to="/vocabs/lv2_vocab.pdf" class="btn-link">
      <button class="btn">level II</button>
    </router-link>
    <router-link to="/vocabs/lv3_vocab.pdf" class="btn-link">
      <button class="btn">level III</button>
    </router-link>
    <router-link to="/vocabs/lv4_vocab.pdf" class="btn-link">
      <button class="btn">level IV</button>
    </router-link>
    <router-link to="/vocabs/lv5_vocab.pdf" class="btn-link">
      <button class="btn">level V</button>
    </router-link>
  </main>
</template>

<style>
main {
  text-align: center;
  padding-top: 150px;
  background-image:
    linear-gradient(#00000055, #00000055), url("../assets/bg_levels.jpg");
  background-size: cover;
  background-position: center;
  min-height: 100vh;
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
.btn-link {
  text-decoration: none;
}

.btn {
  display: block;
  margin: 25px auto;
  padding: 50px 70px;
  width: 500px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 25px;
  font-family: "Trebuchet MS", sans-serif;
  font-weight: bold;
  letter-spacing: 2px;
  color: whitesmoke;
}

.btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: 0.3s;
}
h1 {
  text-align: center;
  color: whitesmoke;
  font-family: Georgia, serif;
  font-weight: bold;
}
</style>

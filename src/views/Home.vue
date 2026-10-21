<script setup>
import { userStore } from "../scripts/store";
import { useRouter } from "vue-router";

const router = useRouter();
const goToLevels = () => {
  router.push("/levels");
};
</script>

<template>
  <main>
    <h1>World Up</h1>
    <article>
      <p id="greeting">
        Greetings, <br />
        Let's learn English!
      </p>
    </article>
    <div id="box">
      Daily progress<br />
      <div class="progress-bar">
        <div class="progress-bar-fill"></div>
        <p>Target: {{ userStore.dailyGoal }} mins</p>
      </div>
    </div>
    <button class="start-btn" @click="goToLevels">Start Learning!</button>
  </main>
</template>

<style scoped>
main {
  text-align: center;
  padding-top: 150px;
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url(../assets/bg_home.jpg);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
}

h1 {
  text-align: center;
  color: whitesmoke;
  font-family: Georgia, serif;
  font-weight: bold;
}
p#greeting {
  color: gainsboro;
  text-align: center;
  margin-top: 50px;
  font-size: 24px;
  font-family: Avenir, sans-serif;
  font-weight: bold;
}
div#box {
  width: 300px;
  padding: 20px;
  height: 150px;
  border-radius: 10px;
  color: aliceblue;
  text-align: center;
  margin: 20px auto;
  border: 1px solid #ffffff66;
  background-color: #ffffff33;
  font-size: 20px;
  font-family: Avenir, sans-serif;
  font-weight: bold;
}
.start-btn {
  display: block;
  margin: 25px auto;
  padding: 12px 30px;
  font-size: 20px;
  font-family: Avenir, sans-serif;
  border: none;
  border-radius: 10px;
  background-color: whitesmoke;
  cursor: pointer;
  transition: 0.1s ease-in-out;
}
.start-btn:hover {
  background-color: #eeeeee;
  transform: scale(1.05);
}
.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #ddd;
  border-radius: 10px;
  overflow: hidden;
  margin: 20px auto;
}
.progress-bar-fill {
  height: 100%;
  width: 0;
  background-color: #4caf50;
  border-radius: 10px;
  transition: width 0.1s linear;
}
</style>

<template>
  <main>
    <h1>World Up</h1>
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

.btn-link {
  text-decoration: none;
}

.btn {
  display: block;
  margin: 25px auto;
  padding: 50px 70px;
  font-size: 20px;
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

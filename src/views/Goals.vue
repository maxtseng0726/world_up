<template>
  <main>
    <h1>Nice to meet you!</h1>

    <div class="goal-selection">
      <h2>Goals:</h2>

      <select>
        <option disabled selected value="">Set your goals</option>
        <option value="15">15 mins</option>
        <option value="20">20 mins</option>
        <option value="25">25 mins</option>
        <option value="30">30 mins</option>
        <option value="35">35 mins</option>
        <option value="40">40 mins</option>
        <option value="45">45 mins</option>
        <option value="50">50 mins</option>
        <option value="55">55 mins</option>
        <option value="60">60 mins</option>
      </select>

      <button class="confirm-btn">Confirm</button>
    </div>
  </main>
</template>

<style scoped>
main {
  text-align: center;
  padding-top: 150px;
  background-image:
    linear-gradient(#00000055, #00000055), url("../assets/bg_goals.jpg");
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  font-family: "courier new", courier, monospace;
  font-weight: 500;
}

.goal-selection {
  margin-top: 30px;
  text-align: center;
  background-color: #ffffff33;
  border-radius: 20px;
  width: 300px;
  border: 1px solid #ffffff66;
  padding: 30px;
  margin: 0 auto;
}

select {
  width: 200px;
  height: 40px;
  font-size: 18px;
  display: block;
  margin: 0 auto 20px auto; /* Centers the select element horizontally */
}

.confirm-btn {
  padding: 10px 20px;
  font-size: 16px;
  width: 200px;
  height: 30px;
  margin-top: 40px;
  border-radius: 10px;
  border: none;
}

.confirm-btn:hover {
  background-color: #202da0;
  color: white;
}
</style>

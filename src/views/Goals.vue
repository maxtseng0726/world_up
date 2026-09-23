<template>
  <main>
    <h1>Nice to meet you!</h1>

    <div class="goal-selection">
      <h2>Goals:</h2>

      <select>
        <option disabled selected value="">Set your goals</option>
        <option value="15">15 min</option>
        <option value="20">20 min</option>
        <option value="25">25 min</option>
        <option value="30">30 min</option>
        <option value="35">35 min</option>
        <option value="40">40 min</option>
        <option value="45">45 min</option>
        <option value="50">50 min</option>
        <option value="55">55 min</option>
        <option value="60">60 min</option>
      </select>

      <button class="confirm-btn">Confirm</button>
    </div>
  </main>
</template>

<style scoped>
main {
  text-align: center;
  padding-top: 150px;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.goal-selection {
  margin-top: 30px;
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
}
</style>

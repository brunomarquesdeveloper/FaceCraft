<template>
  <header class="app-header">
    <div class="header-content">
      <div class="brand">
        <img
          src="/icons/icon-192.png"
          alt="FaceCraft"
          class="brand-logo"
        />

        <span class="brand-name">FaceCraft</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  width: 100%;
  background: #0f1115;
  border-bottom: 1px solid #24272d;
}

.header-content {
  width: 100%;
  max-width: 480px;
  height: 64px;
  margin: 0 auto;
  padding: 0 20px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.brand-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: cover;
}

.brand-name {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
}
</style>
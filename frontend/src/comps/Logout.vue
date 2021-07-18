<template>
  <el-button type="primary" @click="submitLogout()">Logout</el-button>
</template>

<script>
export default {
  methods: {
    submitLogout() {
      this.handleLogout();
    },
    handleLogout() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/');
    },
  },
};
</script>

<style>
</style>


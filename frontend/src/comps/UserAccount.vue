<template>
  <el-row>
    <p>Show user account details</p>
  </el-row>
  <el-row>
    <p>Token: {{ user.access_token }}</p>
  </el-row>
  <el-row>
    <p>User: {{ user.username }}</p>
  </el-row>
  <el-row>
    <Logout />
  </el-row>
</template>

<script>
import Logout from './Logout.vue';
import { mapGetters } from 'vuex'

export default {
  components: {
    Logout,
  },
  computed: {
    ...mapGetters(['auth/user'])
  },
};
</script>

<style>
</style>

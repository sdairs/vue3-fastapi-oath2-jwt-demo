<template>
  <el-row justify="center">
    <el-col :span="6">
      <Login v-if="!isLoggedIn()" />
      <UserAccount v-if="isLoggedIn()" />
    </el-col>
  </el-row>
</template>

<script>
import Login from "../comps/Login.vue";
import UserAccount from "../comps/UserAccount.vue";

export default {
  components: {
    Login,
    UserAccount,
  },
  data() {
    return {};
  },
  methods: {
    isLoggedIn(){
      return this.$store.state.auth.status.loggedIn;
    }
  },
};
</script>

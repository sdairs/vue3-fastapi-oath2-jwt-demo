<template>
  <el-row>
    <el-column>
      <el-form
        :model="loginForm"
        label-width="120px"
      >
        <el-form-item label="Username" prop="username">
          <el-input v-model.number="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="loginForm.password"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitLogin()">Submit</el-button>
        </el-form-item>
      </el-form>
    </el-column>
  </el-row>
</template>

<script>
import { postApi } from "../helper/api";

export default {
  data() {
    return {
      loginForm: {
        password: "",
        username: "",
      },
    };
  },
  methods: {
    submitLogin() {
	this.handleLogin(this.loginForm);
    },
    handleLogin(user) {
      this.$store.dispatch("auth/login", user).then(
        () => {
          this.$router.push("/");
        },
        (error) => {
          this.message =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();
        }
      );
    },
  },
};
</script>

<style>
</style>


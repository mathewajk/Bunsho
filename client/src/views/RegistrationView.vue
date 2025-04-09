<script setup lang="ts">
import { useSessionStore } from '../stores/session'
import { useRouter } from 'vue-router'
const session = useSessionStore()
const router = useRouter()

interface RegistrationForm {
    username: string
    email: string
    password: string
    password_confirm: string
}

const register = (form: RegistrationForm) => {
    console.log(form)
    session.register(form.email, form.username, form.password).then(() => {
        router.push('/login')
    }).catch((error) => {
        console.log(error)
    })
}

const handleIconClick = (node: any, e: any) => {
  node.props.suffixIcon = node.props.suffixIcon === 'eye' ? 'eyeClosed' : 'eye'
  node.props.type = node.props.type === 'password' ? 'text' : 'password'
}

</script>

<template>
    <div class="wrapper">
        <div class="center-button">
            <FormKit type="form" @submit="register">
                <FormKit
                    type="text"
                    name="username"
                    label="Username"
                    help="Input username"
                    required="true"
                />
                <FormKit
                    type="email"
                    name="email"
                    label="Email"
                    help="Input email"
                    required="true"
                />
                <FormKit
                    type="password"
                    name="password"
                    label="Password"
                    help="Input password"
                    required="true"
                    prefix-icon="password"
                    suffix-icon="eyeClosed"
                    @suffix-icon-click="handleIconClick"
                    suffix-icon-class="hover:text-blue-500"
                />
                <FormKit
                    type="password"
                    name="password_confirm"
                    label="Confirm Password"
                    help="Confirm password"
                    required="true"
                    prefix-icon="password"
                    suffix-icon="eyeClosed"
                    @suffix-icon-click="handleIconClick"
                    suffix-icon-class="hover:text-blue-500"
                    validation="confirm|password"
                    validation-message="Passwords do not match"
                />
            </FormKit>
        </div>
    </div>
</template>

<style scoped>
.center-button {
    display: flex;
    justify-content: center;
}

button {
    border: none;
    border-radius: 10px;
    color: white;
    background-color: rgb(0, 107, 189);
    font-size: 2rem;
    padding: 10px;
    cursor: pointer;
    transition: ease-in 0.1s;
}

button:hover {
    background-color: rgb(25, 56, 143);
    transition: ease-in 0.25s;
}
</style>
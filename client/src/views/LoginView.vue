<script setup>
import { useSessionStore } from '../stores/session.ts'
const session = useSessionStore()

const login = (form) => {
    console.log(form)
    session.login(form.username, form.password)
}

const handleIconClick = (node, e) => {
  node.props.suffixIcon = node.props.suffixIcon === 'eye' ? 'eyeClosed' : 'eye'
  node.props.type = node.props.type === 'password' ? 'text' : 'password'
}

</script>

<template>
    <div class="wrapper">
        <div class="center-button">
            <FormKit type="form" @submit="login">
                <FormKit
                    type="text"
                    name="username"
                    label="Username"
                    help="Input username"
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
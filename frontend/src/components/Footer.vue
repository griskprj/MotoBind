<template>
    <div class="wrapper">
        <div class="wrapper-colmns">
            <div class="left-col">
                <div class="logo">
                    <router-link to="/home">
                        <img class="logo-img" src="/MotoBindLogo.png" alt="">
                    </router-link>
                </div>
            </div>
            
            <hr>
    
            <div class="right-col">
                <nav>
                    <router-link class="link-item" to="/lending">MotoBind</router-link>
                    <router-link class="link-item" to="/about">О проекте</router-link>
                    <router-link class="link-item" to="/privacy-policy">Политика конфиденциальности</router-link>
                    <router-link class="link-item" to="/rules">Правила сервиса</router-link>
                </nav>
            </div>
        </div>
        <p class="rules">© 2025 MotoBind. Все права защищены</p>
    </div>
</template>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px;
    
    background-color: var(--bg-primary);

    margin-top: 48px;
}

.wrapper-colmns {
    display: flex;
    flex-direction: row;
    margin-bottom: 32px;

    gap: 32px;
}

.logo-img {
    max-width: 128px;
    max-height: 128px;
    border-radius: 25px;
    box-shadow: 0px 0px 30px 0px rgba(18, 18, 27, 0.3);

    transition: all, 0.3s;
}

.logo-img:hover  {
    box-shadow: 0px 0px 30px 0px rgba(124, 58, 237, 0.3);
}

.right-col nav {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;

    line-height: 30px;
    
}

.link-item {
    color: var(--text-secondary);
}

.link-item:hover {
    color: var(--accent);
}

.rules {
    margin-top: 24px;
    font-weight: 300;
    color: var(--text-muted);

    height: 100%;
}


@media (max-width: 768px) {
    .wrapper-colmns {
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 12px;
    }

    hr {
        min-width: 128px;
    }
}
</style>
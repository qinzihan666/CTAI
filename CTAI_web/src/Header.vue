<template>
    <div id="Header">
        <div class="contact-info">
            <span class="phone">
                <i class="el-icon-phone-outline"></i>免费咨询：010-12345678
            </span>
            <span class="time">
                <i class="el-icon-time"></i>工作时间：8:00-18:00
            </span>
        </div>

        <div id="word">
            <h1>{{ msg }}</h1>
        </div>
    </div>
</template>

<script>
export default {
    name: "Header",
    data() {
        return {
            msg: "直肠肿瘤辅助诊断系统",
            activeIndex: "1"
        };
    }
};
</script>

<style scoped>
#Header {
    padding: 30px 0;
    width: 90%;
    margin: 10px auto;
    position: relative;
    /* 父容器相对定位 */
}

/* 联系方式绝对定位 */
.contact-info {
    position: absolute;
    left: 20px;
    /* 距离左侧距离 */
    top: 30px;
    /* 距离顶部距离 */
    display: flex;
    flex-direction: column;
    gap: 8px;
    /* 两个信息之间的间距 */
}

.contact-info span {
    font-size: 16px;
    color: #999;
    display: flex;
    align-items: center;
}

.phone {
    color: #21b3b9 !important;
    font-weight: bold;
}

.contact-info i {
    font-size: 23px;
    margin-right: 10px;
}

/* 标题居中 */
#word {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    margin: 0;
    height: 60px;
    line-height: 3.2em;
}

h1 {
    color: #21b3b9;
    letter-spacing: 10px;
    font-size: 2.3em;
    text-align: center;
    white-space: nowrap;
    /* 防止文字换行 */
}

i,
input,
label {
    vertical-align: middle;
}

i {
    border: 0;
    display: block;
    cursor: pointer;
}
</style>

<template>
    <b-row>
        <b-col class="hello" cols="12">
            {{greeting}} {{who}}
        </b-col>
        <slot>
            Default slot content, replace with your own text between the component tags.
            See the <a href="https://vuejs.org/v2/guide/components-slots.html" target="_blank">VueJS documentation aaa for slots</a> for more information.
        </slot>
    </b-row>
</template>

<script>
module.exports = {
    /** Allow greeting and who to be passed as parameters but provide defaults
     * @see https://vuejs.org/v2/guide/components-props.html#Prop-Validation
     */
    props: {
        'greeting': {type: String, default: 'Hello'},
         'who': {type: String, default: 'World'},
    },

    /** Any data must be wrapped in a fn to isolate it in case this component is used multiple times */
    data: function() { return {

    }}
}
</script>

<style scoped>
    .hello {
        background-color: #ffe;
        font-size: 2rem;
        text-align: center;
    }
</style>
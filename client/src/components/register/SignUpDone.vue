<template>
	<v-card
		class='pa-3'
		outlined
		width=400
	>
		<v-card-title>
			<h1 class="register_title">仮登録メールを送信しました。</h1>
		</v-card-title>

		<v-col class='text-center' cols='12'>
			<v-btn
				depressed
				x-large
				class='teal lighten-4 ma-3'
				@click='top'
			>TOPへ</v-btn>
		</v-col>

	</v-card>
</template>

<script>
import { Common } from '@/static/js/common'

const Com = new Common()

export default {
  name: 'SignupDone',
  data: () => ({

  }),
  methods: {
    top () {
      this.$router.push('/')
    //   Com.reload(this.$router)
    }
  }
}
</script>

<style lang='scss'>

</style>

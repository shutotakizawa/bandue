<template>
	<v-card
		class='pa-3'
		outlined
		width=400
	>
		<v-card-title>
			<h1 class="register_title">確認画面</h1>
		</v-card-title>

		<v-simple-table>
			<template v-slot:default>
			<tbody>
				<tr>
					<th class="text-left">Name</th>
					<td>{{ data.username }}</td>
				</tr>
				<tr>
					<th class="text-left">EMail</th>
					<td>{{ data.email }}</td>
				</tr>
				<tr>
					<th class='text-left'>Password</th>
					<td>{{ data.password }}</td>
				</tr>
			</tbody>
			</template>
		</v-simple-table>
		<v-form ref='form'>
			<v-col class='text-center' cols='12'>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-3'
					@click='back'
				>戻る</v-btn>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-3'
					@click='signup'
				>SignUp</v-btn>
			</v-col>
		</v-form>
	</v-card>
</template>

<script>
import { Const } from '@/static/js/const'

const Con = new Const()

export default {
  props: ['data'],
  name: 'SignUpConf',
  data: () => ({
    valid: true,
    loading: false
  }),
  methods: {
    signup () {
      console.log('入力情報',this.data)
      this.$axios.post('/api/signup/', this.data)
        .then(res => {
          console.log(res)
		  this.$emit('signup-change-view', Con.SIGNUP_DONE_VIEW)
		  // サインアップ後は、認証完了の状態にするだけでいい？※要検討
          // this.$axios.post('auth/', this.data)
          //   .then(res => {
          //     console.log(res)
			//   // 認証データの設定
			//   this.$store.commit('setToken', { res: res.data, req:res.requestData })
          //   })
          //   .catch(e => {
          //     console.log(e)
          //   })
        })
        .catch(e => {
          console.log(e.response)
        })
    },
    back () {
      this.$emit('signup-change-view', Con.SIGNUP_VIEW)
    }
  }
}
</script>

<style lang='scss'>

</style>

<template>
    <v-container fluid class='search_result_wrap'>
        <v-row>
            <v-col
                cols='12'
            >

        <v-tabs
            v-model='searchTabModel'
            class='search_tab_wrap'
            centered
            fixed-tabs
            color='light-blue lighten-4'
        >
            <v-tab
                v-for='(tab, i) in SearchTabList'
                :key='i'
                :href='`#tab-${i}`'
                @click='tabChange(tab, i)'
            >
                {{ tab }}
            </v-tab>
        </v-tabs>

        <v-tabs-items v-model='searchTabModel'>
            <v-tab-item
                v-for='(tab, i) in SearchTabList'
                :key='i'
                :value="'tab-' + i"
            >
                <!-- ロード中 -->
                <div v-if='loading'>
                    <Loading></Loading>
                </div>

                <!-- 読込後ここから -->
                <div v-else>

                    <!-- ツイート関連ここから -->
                    <div v-if='i != 2'>

                        <!-- ツイート0件以上だったらここから -->
                        <div v-if='tweetList.length > 0'>

                            <!-- ツイートループここから -->
                            <div v-for='(tweet, index) in tweetList' :key='`tweet.author-${index}`'>
                                <v-container fluid>
                                    <v-card
                                        flat
                                        class='tweet_wrap'
                                    >
                                        <div
                                            v-if='tweet.isRetweeted'
                                            class='pt-1 retweet_info'
                                        >
                                            <v-icon
                                                color='green lighten-1'
                                            >mdi-repeat</v-icon>
                                            リツイート済み
                                        </div>
                                        <v-card-title>
                                            <v-row>
                                                <v-col
                                                    cols='auto'
                                                >
                                                    <v-avatar>
                                                        <v-img v-if='tweet.userIcon !== "/media/"' :src='tweet.userIcon'></v-img>
                                						<v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
                                                    </v-avatar>
                                                    <router-link
                                                        @click.native='reload()'
                                                        :to='{ name : "Profile", params : { username: tweet.author }}'
                                                        class='tweet_author z10'
                                                    >{{ tweet.author }}</router-link>
                                                </v-col>
                                                <v-spacer></v-spacer>
                                                <v-col
                                                    cols='auto'
                                                >
                                                    <span class='ml-8' style='font-size:50%;'>{{ tweet.created_time }}</span>
                                                </v-col>
                                            </v-row>
                                        </v-card-title>

                                        <!-- ツイート内容 -->
                                        <v-card-text>
                                            {{ tweet.content }}
                                        </v-card-text>

                                        <div>
                                            <img :src='tweet.images' width="100">
                                        </div>
                                        <v-card-actions>
                                            <v-list-item>
                                                <v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
                                                    <v-list-item-title>{{ tag.title }}</v-list-item-title>
                                                </v-list-item-content>
                                                <v-row
                                                    align='center'
                                                    justify='end'
                                                >
                                                    <reply
                                                        :tweet=tweet
                                                        :isBlocked=tweet.isBlocked
                                                    ></reply>
                                                    <retweet
                                                        :tweet=tweet
                                                        :isBlocked=tweet.isBlocked
                                                    ></retweet>
                                                    <like
                                                        :tweet=tweet
                                                        :isBlocked=tweet.isBlocked
                                                    ></like>
                                                </v-row>
                                            </v-list-item>
                                        </v-card-actions>
                                    </v-card>
                                </v-container>
                            </div>
                            <!-- ツイートループここまで -->

                            <!-- 次ページが存在したらここから -->
                            <div v-if='nextPage != null'>
                                <div v-if='!loadingMore'>
                                    <v-btn
                                    class='load_more'
                                    @click=next
                                    >ツイートを更に読み込む</v-btn>
                                </div>
                                <div v-else>
                                    <Loading></Loading>
                                </div>
                            </div>
                            <!-- 次ページが存在したらここまで -->

                        </div>
                        <!-- ツイート0件以上だったらここまで -->

                        <!-- ツイートが0件だったら -->
                        <div v-else>
                            <v-card
                                flat
                                class='tweet_not_found_wrap'
                            >
                                <v-card-title
                                    class='tweet_not_found'
                                >
                                    ツイートが見つかりません。
                                </v-card-title>
                            </v-card>
                        </div>
                        <!-- ツイートが0件だったらここまで -->

                    </div>
                    <!-- ツイート関連ここまで -->

                    <!-- ユーザー関連ここから -->
                    <div v-else>

                        <!-- ユーザーが0件以上だったらここから -->
                        <div v-if='userList.length > 0'>

                            <!-- ユーザーループここから -->
                            <div v-for='(user, index) in userList' :key='`user.username-${index}`'>

                                <!-- ブロックされていなければユーザーを表示 -->
                                <div v-if='!user.isBlocked'>
                                    <v-card
                                        flat
                                        class='user_wrap'
                                        height='200px'
                                    >
                                        <v-card-title
                                            class='username_wrap'
                                        >
                                            <v-row>
                                                <v-col
                                                    cols='auto'
                                                >
                                                    <v-avatar>
                                                        <v-img v-if='user.icon !== null' :src='user.icon'></v-img>
                                                        <v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
                                                    </v-avatar>
                                                    <router-link
                                                        @click.native='reload()'
                                                        :to='{ name : "Profile", params : { username: user.username}}'
                                                        class='username z10'
                                                    >{{ user.username | truncate(12, '..') }}</router-link>
                                                </v-col>
                                                <v-spacer></v-spacer>
                                                <v-col
                                                    cols='auto'
                                                >
                                                    <follow
                                                        :followBtnStyleObject='followBtnStyleObject'
                                                        :profileData='user'
                                                    ></follow>
                                                </v-col>
                                            </v-row>
                                        </v-card-title>
                                        <v-card-text>
                                            {{ user.introduction | truncate(60) }}
                                        </v-card-text>
                                    </v-card>
                                </div>
                                <!-- ブロックされていなければユーザー表示ここまで -->

                            </div>
                            <!-- ユーザーループここまで -->

                            <!-- 次ページが存在したらここから -->
                            <div v-if='nextPage != null'>
                                <div v-if='!loadingMore'>
                                    <v-btn
                                        class='load_more'
                                        @click=next
                                    >ユーザーを更に読み込む</v-btn>
                                </div>
                                <div v-else>
                                    <Loading></Loading>
                                </div>
                            </div>
                            <!-- 次ページが存在したらここまで -->

                        </div>
                        <!-- ユーザーが0件以上だったらここまで -->

                        <!-- ユーザー0件だったらここから -->
                        <div v-else>
                            <v-card
                                flat
                                class='user_not_found_wrap'
                            >
                                <v-card-title
                                    class='user_not_found'
                                >
                                    ユーザーが見つかりません。
                                </v-card-title>
                            </v-card>
                        </div>
                        <!-- ユーザー0件だったらここまで -->

                    </div>
                    <!-- ユーザー関連ここまで -->

                </div>
                <!-- 読込後ここまで -->

            </v-tab-item>
        </v-tabs-items>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

    import Reply from '@/components/common/Reply'
    import Retweet from '@/components/common/Retweet'
    import Like from '@/components/common/Like'
    import Follow from '@/components/common/Follow'
    import Loading from '@/components/common/Loading'
    import _ from 'lodash'
    import { Common } from '@/static/js/common'

    const Com = new Common()

    export default {
        name: 'SearchResult',

        props: {
            'searchText': {
                type: String,
                required: true
            }
        },

        components: {
            Reply,
            Retweet,
            Like,
            Follow,
            Loading,
        },

        data: () => ({
            searchTabModel: null,
            SearchTabList: [
                'Trand',
                'New',
                'User',
                'Media'
            ],
            tweetList: [],
            userList: [],
            searchFlg: 0,
            loading: true,
            nextPage: null,
            loadingMore: false,
            followBtnStyleObject: {
                width: '90px',
                height: '30px',
                fontSize: '10px',
                marginTop: '8px',
            },
        }),

        created () {
            this.$watch(
                () => [this.searchFlg, this.searchText], (val) => {
                    console.log('searchFlg, searchText => ' + val)
                    this.search(...val)
                    this.loading = true
                }
            )
        },

        mounted: function () {
            this.search(this.searchFlg, this.searchText)
            this.loading = true

        },

        methods: {
            tabChange (tab, i) {
                this.searchFlg = i
            },

            search: _.debounce(function search(searchFlg, searchText) {
                // 空白削除し、カンマ区切りの文字列で送る
                var trimedText = this.trim(searchText)
                var trimedTextList = [...new Set(trimedText.split(/\s+/))]
                var searchWord = trimedTextList.join(',')
                console.log('検索文字列 : ' + searchWord)
                this.$axios.get('/api/search/', {
                    params: {
                        searchFlg: searchFlg,
                        searchText: searchWord
                    }
                })
                .then(res => {
                    console.log(res.data)
                    if (this.searchFlg !== 2) {
                        for (var i in res.data.results) {
                            var updatedAt = res.data.results[i].updated_at.substr(0, 10)
                            res.data.results[i].updated_at = updatedAt
                        }
                        this.tweetList = res.data.results
                        console.log('ツイート一覧', this.tweetList)
                    } else {
                        this.userList = res.data.results
                        console.log('ユーザー一覧', this.userList)
                    }
                        this.nextPage = res.data.next
                        this.loading = false
                })
                .catch(e => {
                    console.log(e)
                    this.loading = false
                })
            }, 200),

            trim (word) {
                return String(word).replace(/^\s+|\s+$/g, '')
            },

            next () {
                if (this.nextPage !== null) {
                    this.loadingMore = true
                    this.$axios.get(this.nextPage)
                    .then(res => {
                        if (this.searchFlg !== 2) {
                            for (var i in res.data.results) {
                                var updatedAt = res.data.results[i].updated_at.substr(0, 10)
                                res.data.results[i].updated_at = updatedAt
                                this.tweetList.push(res.data.results[i])
                            }
                            console.log('ツイート一覧', this.tweetList)
                        } else {
                            this.userList.push(res.data.results)
                            console.log('ユーザー一覧', this.userList.results)
                        }

                        this.nextPage = res.data.next
                        this.loadingMore = false
                    })
                    .catch(e => {
                        console.log(e)
                    })
                }
            },

            reload () {
                // Com.reload(this.$router)
            }
        }
    }

</script>

<style lang='scss'>
  .search_result_wrap {
    max-width: 100%;
    height: 690px;
    overflow: auto;

    .tweet_wrap {
      cursor: pointer;
      .tweet_author {
        position: relative;
      }

    }

    .user_wrap {

      .username_wrap {

        .username {
          font-size: 18px;
          text-decoration: none;
          color: black;
        }

      }
    }

    .load_more {
      display: block;
      margin: 20px auto;
    }

    .tweet_not_found_wrap {
        .tweet_not_found {
            font-size: 16px;
        }
    }

    .user_not_found_wrap {
        .user_not_found {
            font-size: 16px;
        }
    }
  }
</style>

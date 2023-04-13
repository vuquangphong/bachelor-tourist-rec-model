<template>
  <div class="home-container">
    <div class="left-bar-container">
      <LeftBar />
    </div>

    <div class="main-content">
      <div class="user-detail">
        <div class="title">Thông tin người dùng</div>

        <div class="content">
          <div class="left">
            <div class="username">
              <label for="username">Tên người dùng</label>
              <input
                type="text"
                id="username"
                v-model="userReference.username"
              />
            </div>
            <div class="destination">
              <label for="destination">Điểm đến (Tỉnh/TP)</label>
              <input
                type="text"
                id="destination"
                v-model="userReference.destination"
              />
            </div>

            <div class="submit-btn">
              <button @click="userRefSubmit">Xác nhận</button>
            </div>
          </div>

          <div class="right">
            <div class="time">
              <label for="num-days">Số ngày đi</label>
              <select
                name="num-days"
                id="num-days"
                v-model="userReference.numberOfDays"
              >
                <option
                  v-for="(num, index) in dataNumDays"
                  :key="index"
                  :value="num"
                >
                  {{ num }} ngày
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="categories-container" v-if="dataCategories.length > 0">
        <div class="title">
          <div class="main-title">Chọn các tiện nghi của khách sạn</div>
          <div class="detail-title">
            Chọn ít nhất 5 tiện nghi mà bạn mong muốn khách sạn có:
          </div>
        </div>

        <div class="option-categories">
          <div
            class="options-container"
            v-for="(cate, index) in dataCategories"
            :key="index"
          >
            <input
              type="checkbox"
              :name="cate"
              :id="index"
              :value="cate"
              @input="handleChooseCategories"
            />
            <label :for="index">{{ cate }}</label>
          </div>
        </div>

        <div class="submit-btn">
          <button @click="submitCategories">Xác nhận</button>
        </div>
      </div>

      <div class="final-output" v-if="dataFinal.length > 0">
        <div class="big-title">Đề xuất của chúng tôi</div>

        <div class="output-container">
          <div
            class="output-single-day"
            v-for="(hotel, index) in dataFinal"
            :key="index"
          >
            <div class="title-2">Khách sạn {{ index + 1 }}</div>
            <div class="place-container">
              <div class="place-name">
                <span class="key">TÊN KHÁCH SẠN </span>
                <span class="value">{{ hotel.name }}</span>
              </div>
              <div class="place-price">
                <span class="key">GIÁ TRUNG BÌNH </span>
                <span class="value">{{
                  hotel["avg_price"] <= 0
                    ? "Không có thông tin"
                    : hotel["avg_price"]
                }}</span>
              </div>
              <div class="place-location">
                <span class="key">ĐIỂM ĐÁNH GIÁ </span>
                <span class="value">{{ hotel.rating }}</span>
              </div>

              <div class="place-rating">
                <span class="key">TRẢI NGHIỆM </span>
                <span class="value">{{ hotel.experience }}</span>
              </div>
              <div class="place-rating">
                <span class="key">VỊ TRÍ </span>
                <span class="value">{{ hotel.location }}</span>
              </div>
              <div class="place-rating">
                <span class="key">ĐỊA CHỈ </span>
                <span class="value">{{ hotel.address }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="wishing">
          Chúc các bạn có một chuyến đi vui vẻ và đáng nhớ!
        </div>
      </div>
    </div>

    <div class="loading">
      <Loader :isLoading="isLoading" />
    </div>
  </div>
</template>

<script>
import { reactive, toRefs } from "vue";
import LeftBar from "@/components/LeftBar.vue";
import Loader from "@/components/LoaderLoading.vue";
import { getDataApi, postDataApi } from "@/utils/fetchApi";

export default {
  components: { LeftBar, Loader },

  setup() {
    const state = reactive({
      userReference: {
        username: "",
        destination: "",
        numberOfDays: 0,
      },

      dataNumDays: [1, 2, 3, 4],

      dataCategories: [],

      dataCategoriesPreference: [],

      dataFinal: [],

      isLoading: false,
    });

    return { ...toRefs(state) };
  },

  methods: {
    async userRefSubmit() {
      this.isLoading = true;

      try {
        const res = await getDataApi("/hotels/amenities");
        this.dataCategories = res.data;
        this.isLoading = false;
      } catch (err) {
        this.isLoading = false;
        console.log(err);
      }
    },

    handleChooseCategories(event) {
      if (event.target.checked) {
        this.dataCategoriesPreference.push(event.target._value);
      } else {
        this.dataCategoriesPreference = this.dataCategoriesPreference.filter(
          (cate) => cate !== event.target._value
        );
      }
    },

    async submitCategories() {
      if (this.dataCategoriesPreference.length < 5) {
        alert("Bạn hãy chọn ít nhất 5 độ tiện nghi");
      } else {
        this.isLoading = true;

        let payload = {
          city: this.userReference.destination,
          number_of_days: this.userReference.numberOfDays,
          user_name: this.userReference.username,
          amenities_pref: this.dataCategoriesPreference,
        };

        try {
          const res = await postDataApi("/hotels", payload);
          this.dataFinal = res.data;
          this.isLoading = false;
        } catch (err) {
          this.isLoading = false;
          console.log(err);
        }
      }
    },
  },
};
</script>

<style scoped>
.home-container {
  display: flex;
}

.left-bar-container {
  height: 100vh;
  padding: 12px;
  /* border-right: 1px solid rgba(0, 0, 0, 0.2); */
}

.main-content {
  width: 100%;
  border-left: 1px solid rgba(0, 0, 0, 0.2);
}

.user-detail,
.categories-container {
  padding: 20px;
}

.user-detail .title,
.categories-container .main-title,
.final-output .big-title {
  font-size: x-large;
  font-weight: 600;
  padding-bottom: 10px;
}

.user-detail .content {
  display: flex;
}

.user-detail .content .left {
  margin-right: 90px;
}

.user-detail .content .username,
.user-detail .content .time {
  margin-bottom: 5px;
}

.user-detail .content .username label,
.user-detail .content .time label {
  padding-right: 40px;
}

.user-detail .content .destination,
.rating-categories {
  margin-bottom: 10px;
}

.user-detail .content .destination label {
  padding-right: 15px;
}

select#destination {
  width: 164px;
}

select#num-days {
  width: 163px;
}

.user-detail .content .budget label {
  padding-right: 9px;
}

.categories-container .detail-title {
  font-size: medium;
  font-weight: 600;
  padding-bottom: 10px;
}

.option-categories {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.option-categories .options-container {
  flex: 1 210px;
}

.rating-container label {
  padding-right: 10px;
}

.rating-container span {
  padding-left: 10px;
}

.final-output {
  padding: 20px;
}

.final-output .title-1 {
  font-size: large;
  font-weight: 600;
  padding-bottom: 10px;
}

.final-output .title-2 {
  font-size: medium;
  font-weight: 600;
  padding-bottom: 5px;
  text-decoration: underline;
}

.final-output .main-rec {
  display: flex;
}

.final-output .main-rec .place-container-left {
  min-width: 500px;
  width: 500px;
}

.final-output span.key {
  font-weight: 600;
  display: inline-block;
  width: 170px;
}

.output-single-day {
  margin-bottom: 30px;
}

.rec-first {
  margin-bottom: 15px;
}
</style>
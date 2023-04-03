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

      <div class="categories-container">
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
            <input type="checkbox" :name="cate" :id="index" />
            <label :for="index">{{ cate }}</label>
          </div>
        </div>

        <div class="submit-btn">
          <button @click="submitCategories">Xác nhận</button>
        </div>
      </div>

      <div class="final-output">
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
  </div>
</template>

<script>
import { reactive, toRefs } from "vue";
import LeftBar from "@/components/LeftBar.vue";

export default {
  components: { LeftBar },

  setup() {
    const state = reactive({
      userReference: {
        username: "",
        destination: "",
        numberOfDays: 0,
      },

      dataNumDays: [1, 2, 3, 4],

      dataCategories: [
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
        "category 1",
      ],

      dataCategoriesPreference: [
        {
          name: "category 1",
          rating: 5,
          id: "9dee6f59-d06e-11ed-8957-aa2db87e6710",
        },
        {
          name: "category 1",
          rating: 5,
          id: "c83002cb-d06e-11ed-bfc4-aa2db87e6710",
        },
        {
          name: "category 1",
          rating: 5,
          id: "cf7b1fe6-d06e-11ed-bd7c-aa2db87e6710",
        },
        {
          name: "category 1",
          rating: 5,
          id: "d9042c60-d06e-11ed-b085-aa2db87e6710",
        },
        {
          name: "category 1",
          rating: 5,
          id: "e01c314d-d06e-11ed-b43c-aa2db87e6710",
        },
      ],

      dataRawFinal: {
        timeofday: [
          "Morning",
          "Morning",
          "Evening",
          "Evening",
          "Morning",
          "Morning",
          "Evening",
          "Evening",
        ],
        image: [],
        name: [
          "Cháo Hồng Lương Sử",
          "Nguyen Art Gallery - Vietnam Artworks & Paintings",
          "PHỞ GÀ VĂN MIẾU 17",
          "Cafe Goethe",
          "Cộng Cà Phê đường Điện Biên Phủ",
          "Bảo tàng Lịch sử Quân sự Việt Nam",
          "Vườn hoa Lênin",
          "Bảo tàng Mỹ thuật Việt Nam",
        ],
        location: [
          [21.0252021, 105.8361315],
          [21.0279933, 105.8362406],
          [21.0289115, 105.8375611],
          [21.0304661, 105.8366466],
          [21.0339522, 105.8379675],
          [21.0325549, 105.8393124],
          [21.0315717, 105.8392123],
          [21.0306889, 105.837908],
        ],
        avg_price: [0, 0, 0, 0, 0, 0, 0, 0],
        rating: [4.3, 4.7, 4.7, 4.2, 4.2, 4.2, 4.3, 4.2],
        category: [
          "Ẩm thực, nghỉ ngơi",
          "Triển lãm, nghệ thuật",
          "Ẩm thực, nghỉ ngơi",
          "Đồ uống, thư giãn",
          "Đồ uống, thư giãn",
          "Văn hóa, lịch sử, nghệ thuật",
          "Đi dạo, ngắm cảnh",
          "Văn hóa, lịch sử, nghệ thuật",
        ],
      },

      dataFinal: [
        {
          name: "Cháo Hồng Lương Sử",
          location: [21.0252021, 105.8361315],
          address: "tây hồ",
          avg_price: 0,
          rating: 4.3,
          experience: "Excellent",
        },
        {
          name: "Cháo Hồng Lương Sử",
          location: [21.0252021, 105.8361315],
          address: "tây hồ",
          avg_price: 0,
          rating: 4.3,
          experience: "Excellent",
        },
      ],
    });

    return { ...toRefs(state) };
  },

  methods: {
    userRefSubmit() {
      console.log(this.userReference);
    },

    submitCategories() {
      console.log(this.dataCategoriesPreference);
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
  margin-right: 80px;
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
// c:\users\31194\desktop\毕设（polar codes）\bytedance_microapp\first_demo\pages\jump\jump
Page({
  data: {

  },
  onLoad: function (options) {
    tt.navigateBack({
      delta: 1,
      success(res) {
        console.log(res);
      },
      fail(res) {
        console.log("navigateBack调用失败");
      },
    });
  }
})
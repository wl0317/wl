document.addEventListener('DOMContentLoaded', () => {
  const selectOption = document.getElementById('selectOption');
  const option1 = document.getElementById('option1');
  const option2 = document.getElementById('option2');
  const option3 = document.getElementById('option3');
  const option4 = document.getElementById('option4');

  //充值红豆
  const uidInput = document.getElementById('uid');
  const goldInput = document.getElementById('gold');
  const confirmBtn1 = document.getElementById('confirmBtn1');
  // 开通会员按钮
  const uid1Input = document.getElementById('uid1');
  const confirmBtn2 = document.getElementById('confirmBtn2');
  //失效会员按钮
  const uid3Input = document.getElementById('uid3');
  const confirmBtn3 = document.getElementById('confirmBtn3');
  //修改账户经验值
  const uid4Input = document.getElementById('uid4');
  const expInput = document.getElementById('exp');
  const confirmBtn4 = document.getElementById('confirmBtn4');
  //主播认证
  const uid5Input = document.getElementById('uid5');
  const confirmBtn5 = document.getElementById('confirmBtn5');

  const input3 = document.getElementById('input3');
  const inputOther = document.getElementById('inputOther');



  // 监听选项变化
  selectOption.addEventListener('change', function () {
    const selectedValue = selectOption.value;

    // 重置所有输入框的内容
    resetInputs();

    // 根据选项显示对应输入框
    toggleOptions(selectedValue);
  });

  // 充值红豆逻辑
  confirmBtn1.addEventListener('click', async function () {
    const uid = uidInput.value.trim();
    const gold = goldInput.value.trim();

    if (!uid || !gold) {
      alert('请输入完整信息');
      return;
    }

    try {
      const response = await fetch('http://60.205.59.6:8877/add_gold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ gold: gold, uid: uid })
      });

      const data = await response.json();

      if (data.code === '200') {
        alert('成功: ' + data.message);
      } else {
        alert('失败: ' + data.message);
      }
    } catch (error) {
      alert('请求失败，请检查输入');
      console.error(error);
    }
  });

  // 开通会员逻辑
  confirmBtn2.addEventListener('click', async function () {
    const uid1 = uid1Input.value.trim();

    if (!uid1) {
      alert('请输入开通的UID');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/add/vip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ uid: uid1 })
      });

      const data = await response.json();

      if (data.code === '200') {
        alert('成功: ' + data.message);
      } else {
        alert('失败: ' + data.message);
      }
    } catch (error) {
      alert('请求失败，请检查输入');
      console.error(error);
    }
  });

  //失效会员逻辑
  confirmBtn3.addEventListener('click', async function () {
    const uid3 = uid3Input.value.trim();

    if (!uid3) {
      alert('请输入要失效的UID');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/del/vip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ uid: uid3 })
      });

      const data = await response.json();

      if (data.code === '200') {
        alert('成功: ' + data.message);
      } else {
        alert('失败: ' + data.message);
      }
    } catch (error) {
      alert('请求失败，请检查输入');
      console.error(error);
    }
  });

  //修改账户经验值
  confirmBtn4.addEventListener('click', async function () {
    const uid4 = uid4Input.value.trim();//uid
    const expValue = expInput.value.trim();//经验值

    if (!uid4 || !expValue) {
    alert('请输入完整信息：UID 和 经验值');
    return;
  }


    try {
      const response = await fetch('http://127.0.0.1:5000/add/exp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ uid: uid4, exp: expValue})
      });

      const data = await response.json();

      if (data.code === '200') {
        alert('成功: ' + data.message);
      } else {
        alert('失败: ' + data.message);
      }
    } catch (error) {
      alert('请求失败，请检查输入');
      console.error(error);
    }
  });

  //主播认证
  confirmBtn5.addEventListener('click', async function () {
    const uid5 = uid5Input.value.trim();//uid

    if (!uid5) {
    alert('请输入要认证主播的UID');
    return;
  }

    try {
      const response = await fetch('http://127.0.0.1:5000/anchor/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ uid: uid5})
      });

      const data = await response.json();

      if (data.code === '200') {
        alert('成功: ' + data.message);
      } else {
        alert('失败: ' + data.message);
      }
    } catch (error) {
      alert('请求失败，请检查输入');
      console.error(error);
    }
  });

   // 重置所有输入框内容
  function resetInputs() {
    // 在重置之前检查元素是否存在
    if (uidInput) uidInput.value = '';
    if (goldInput) goldInput.value = '';
    if (uid1Input) uid1Input.value = '';
    if (uid3Input) uid3Input.value = '';
    if (uid4Input) uid4Input.value = '';
    if (uid5Input) uid5Input.value = '';
    if (expInput) expInput.value = '';    // 重置 exp 输入框
    if (input3) input3.value = '';
    if (inputOther) inputOther.value = '';
  }

  // 根据选项显示或隐藏输入框
  function toggleOptions(option) {
    option1.style.display = option === 'option1' ? 'block' : 'none';
    option2.style.display = option === 'option2' ? 'block' : 'none';
    option3.style.display = option === 'option3' ? 'block' : 'none';
    option4.style.display = option === 'option4' ? 'block' : 'none';
    option5.style.display = option === 'option5' ? 'block' : 'none';
  }
});

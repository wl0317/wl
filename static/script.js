document.addEventListener('DOMContentLoaded', () => {
  const selectOption = document.getElementById('selectOption');
  const option1 = document.getElementById('option1');
  const option2 = document.getElementById('option2');
  const option3 = document.getElementById('option3');
  const uidInput = document.getElementById('uid');
  const goldInput = document.getElementById('gold');
  const input3 = document.getElementById('input3');
  const inputOther = document.getElementById('inputOther');
  const confirmBtn1 = document.getElementById('confirmBtn1');

  // 监听选项变化
  selectOption.addEventListener('change', () => {
    resetInputs();
    toggleOptions(selectOption.value);
  });

  // 点击确认按钮处理 Option 1
  confirmBtn1.addEventListener('click', async () => {
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
        body: new URLSearchParams({ gold, uid })
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

  // 重置输入框内容
  function resetInputs() {
    uidInput.value = '';
    goldInput.value = '';
    input3.value = '';
    inputOther.value = '';
  }

  // 根据选项显示对应输入框
  function toggleOptions(option) {
    option1.style.display = option === 'option1' ? 'block' : 'none';
    option2.style.display = option === 'option2' ? 'block' : 'none';
    option3.style.display = option === 'option3' ? 'block' : 'none';
  }
});

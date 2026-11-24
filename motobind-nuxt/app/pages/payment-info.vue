<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

useSeoMeta({
  title: 'Оплата и возврат — MotoBind',
  description: 'Условия оплаты дополнительных мест в гараже MotoBind и порядок возврата средств.',
})
</script>

<template>
  <div class="payment-info-page">
    <div class="container">
      <h1>Оплата и возврат</h1>
      
      <section>
        <h2>Описание услуги и цена</h2>
        <p>
          Сервис MotoBind предоставляет возможность добавить в личный гараж мотоциклы. 
          Одно место в гараже предоставляется <strong>бесплатно</strong>. 
          Дополнительные места можно приобрести за <strong>49 рублей</strong> за одно место (разовый платёж).
        </p>
        <p>
          Каждая успешная покупка увеличивает лимит мотоциклов в вашем аккаунте на один. 
          Автоматических или периодических списаний нет.
        </p>
      </section>

      <section>
        <h2>Как оплатить</h2>
        <p>
          Оплата производится через платёжный сервис <strong>Robokassa</strong>. 
          После нажатия кнопки «Купить место» вы будете перенаправлены на защищённую страницу оплаты. 
          Заказ считается оплаченным после подтверждения платежа платёжным сервисом.
        </p>
        <p>
          Чек формируется в соответствии с правилами применения налога на профессиональный доход (НПД) 
          и направляется на вашу электронную почту.
        </p>
      </section>

      <section>
        <h2>Как получить услугу</h2>
        <p>
          Услуга оказывается дистанционно. После подтверждения оплаты дополнительное место 
          автоматически активируется в вашем аккаунте. 
          Если место не появилось в течение 10 минут, напишите на 
          <a href="mailto:griskyy@yandex.ru">griskyy@yandex.ru</a>, указав email аккаунта и номер заказа.
        </p>
      </section>

      <section>
        <h2>Возврат средств и отказ от услуги</h2>
        <p>
          Вы вправе отказаться от услуги и запросить возврат средств в соответствии с законодательством РФ.
        </p>
        <p><strong>Пошаговый порядок возврата:</strong></p>
        <ol>
          <li>Напишите на электронную почту <a href="mailto:griskyy@yandex.ru">griskyy@yandex.ru</a>.</li>
          <li>В письме укажите: email аккаунта MotoBind, номер заказа и дату платежа.</li>
          <li>Мы рассмотрим обращение в течение <strong>10 рабочих дней</strong> и уведомим вас о решении.</li>
          <li>Если возврат одобрен, денежные средства будут возвращены тем же способом, которым была произведена оплата, в течение <strong>10 рабочих дней</strong> после одобрения.</li>
        </ol>
        <p>
          Обратите внимание: возврат производится в полном объёме. 
          Комиссии платёжного сервиса или банка не удерживаются.
        </p>
      </section>

      <section>
        <h2>Реквизиты исполнителя</h2>
        <p>
          <strong>Исполнитель:</strong> Апольский Григорий Михайлович<br>
          <strong>Статус:</strong> плательщик налога на профессиональный доход (НПД)<br>
          <strong>ИНН:</strong> 236704798600<br>
          <strong>Город:</strong> Сочи<br>
          <strong>Телефон:</strong> +7 988 405-91-11<br>
          <strong>Email:</strong> <a href="mailto:griskyy@yandex.ru">griskyy@yandex.ru</a>
        </p>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.payment-info-page {
  padding: var(--space-8) 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

h1 {
  font-size: var(--text-3xl);
  font-weight: var(--fw-bold);
  margin-bottom: var(--space-6);
}

h2 {
  font-size: var(--text-xl);
  font-weight: var(--fw-semibold);
  margin-top: var(--space-6);
  margin-bottom: var(--space-3);
}

p, li {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-2);
}

ol {
  padding-left: var(--space-5);
  margin-bottom: var(--space-3);
}

a {
  color: var(--color-brand);
  text-decoration: underline;
}
</style>
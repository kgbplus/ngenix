# Тестовое задание Ngenix

1. Утилита create_files.py создает 50 архивов по 100 xml файлов в каждом, 
принимает на вход необязательным параметром путь, где эти файлы нужно создать.
Количество архивов и файлов в них захардкожены константами внутри.
Если файлы уже существуют - перезаписывает их без предупреждения.

2. Утилита process_files.py обрабатывает созданные файлы, на выходе создает
levels.csv и objects.csv с необходимой информацией. Также принимает на вход 
необязательным параметром путь, где лежат архивы и там же создает
результирующие файлы. Если файлы уже существуют - перезаписывает их без 
предупреждения.

3. Обработчик последовательно перебирает файлы архивов (для простоты я считаю,
что в директории необходимо обработать все архивы и все они содержат только 
валидные xml файлы). Распараллеливать обработку архивов не считаю необходимым,
т.к. количество файлов внутри архива сильно превышает среднее число ядер
процессора и я смогу распараллелить обработку внутри каждого архива, без 
существенных потерь в производительности. В тоже время, сама по себе распаковка
архива - это IO операция, которая плохо поддается ускорению параллелизацией.

4. То же самое соображение при чтении отдельных архивов. Я вряд ли добьюсь 
серьезного ускорения если буду читать xml файлы в несколько потоков, в тоже время
это создаст дополнительные сложности (необходимость контролировать создание
временных директорий и распаковку архивов и передавать эту информацию внутрь
подпроцессов).

5. Наконец, не стал распараллеливать писателя выходных файлов по той причине, что
предложенный механизм сборки информации для выходных файлов вполне адекватный по 
потреблению памяти в рамках поставленной задачи, кроме того межпроцессное 
взаимодействие между обработчиками и писателем наоборот внесло бы дополнительные
задержки в работу программы. Такую доработку необходимо делать только в случае,
когда мы боимся, что обработка занимает существенное время, может не завершиться 
вовремя или не завершиться из-за ошибки и нам важно сохранить накопленные данные.

6. Можно еще чуть чуть ускорить выполнение, если использовать map_async вместо
map (на самом деле для указанных в задаче условий и 8 ядерного процессора 
ускорение может составить порядка 5%). Изначально так и сделал, но потом отказался 
от этого в пользу читаемости кода.

7. По опыту тестирования данной программы могу сказать, что основные временные
затраты происходят на операциях ввода вывода. После "прогрева" дискового кэша
скорость выполнения на моем компьютере увеличивается в 3-4 раза. Решить одним
только кодом эту проблему нельзя, она комплексная.

7. Использовал Python 3.7. Заняло около 5 часов.

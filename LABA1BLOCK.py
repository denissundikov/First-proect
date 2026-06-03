import hashlib
import json
import time
from typing import Any, Dict, Optional

class Block:
    """
    Класс, представляющий блок в блокчейне.
    
    Атрибуты:
        index (int): Порядковый номер блока в цепочке
        timestamp (float): Время создания блока
        data (str): Данные, хранящиеся в блоке
        previous_hash (str): Хеш предыдущего блока в цепочке
        nonce (int): Случайное число для майнинга (в данной задаче не используется для Proof of Work)
        hash (str): Хеш текущего блока
    """
    
    def __init__(self, index: int, data: str, previous_hash: str = ""):
        """
        Инициализация нового блока.
        
        Args:
            index: Индекс блока в цепочке
            data: Данные для хранения в блоке
            previous_hash: Хеш предыдущего блока
        """
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Вычисляет SHA-256 хеш текущего блока на основе его полей.
        
        Returns:
            str: Хеш блока в шестнадцатеричном формате
        """
        # Создаем строку из всех полей блока для хеширования
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        
        # Вычисляем SHA-256 хеш
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует блок в словарь для удобного вывода.
        
        Returns:
            Dict[str, Any]: Словарь с данными блока
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    def __str__(self) -> str:
        """Строковое представление блока для вывода."""
        return json.dumps(self.to_dict(), indent=2, default=str)

class Blockchain:
    """
    Класс, представляющий простую блокчейн-цепочку.
    """
    
    def __init__(self):
        """Инициализация блокчейна с генезис-блоком."""
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self) -> Block:
        """
        Создает первый блок в цепочке (генезис-блок).
        
        Returns:
            Block: Генезис-блок
        """
        return Block(0, "Genesis Block", "0")
    
    def get_latest_block(self) -> Block:
        """
        Возвращает последний блок в цепочке.
        
        Returns:
            Block: Последний блок
        """
        return self.chain[-1]
    
    def add_block(self, data: str) -> Block:
        """
        Добавляет новый блок в цепочку.
        
        Args:
            data: Данные для нового блока
            
        Returns:
            Block: Созданный блок
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> tuple[bool, Optional[str]]:
        """
        Проверяет целостность всей цепочки блоков.
        
        Returns:
            tuple[bool, Optional[str]]: (валидна ли цепочка, сообщение об ошибке если не валидна)
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Проверка 1: Корректен ли хеш текущего блока
            if current_block.hash != current_block.calculate_hash():
                return False, f"Неверный хеш блока {current_block.index}"
            
            # Проверка 2: Совпадает ли previous_hash текущего блока с хешем предыдущего
            if current_block.previous_hash != previous_block.hash:
                return False, f"Нарушена связь между блоком {previous_block.index} и блоком {current_block.index}"
        
        return True, "Цепочка валидна"
    
    def display_chain(self) -> None:
        """Выводит информацию о всех блоках в цепочке."""
        print("\n" + "="*50)
        print("СОДЕРЖИМОЕ БЛОКЧЕЙНА")
        print("="*50)
        
        for block in self.chain:
            print(f"\nБлок #{block.index}")
            print(f"Временная метка: {time.ctime(block.timestamp)}")
            print(f"Данные: {block.data}")
            print(f"Хеш предыдущего блока: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Хеш текущего блока: {block.hash}")
            print("-"*50)

def main():
    """
    Основная функция для демонстрации работы блокчейна.
    """
    print("СОЗДАНИЕ ПРОСТОГО БЛОКЧЕЙНА")
    print("="*50)
    
    # Создаем блокчейн
    blockchain = Blockchain()
    
    # Добавляем 5 блоков с различными данными
    test_data = [
        "Первый блок после генезиса",
        "Второй блок с транзакцией",
        "Третий блок с данными",
        "Четвертый блок с информацией",
        "Пятый блок в цепочке"
    ]
    
    for i, data in enumerate(test_data, 1):
        print(f"\nДобавление блока {i}...")
        block = blockchain.add_block(data)
        print(f"Блок {i} добавлен. Хеш: {block.hash[:20]}...")
    
    # Выводим всю цепочку
    blockchain.display_chain()
    
    # Проверяем целостность цепочки
    print("\n" + "="*50)
    print("ПРОВЕРКА ЦЕЛОСТНОСТИ ЦЕПОЧКИ")
    print("="*50)
    
    is_valid, message = blockchain.is_chain_valid()
    print(f"Результат: {'✅ Цепочка валидна' if is_valid else '❌ ' + message}")
    
    # Демонстрация обнаружения подделки
    print("\n" + "="*50)
    print("ДЕМОНСТРАЦИЯ ОБНАРУЖЕНИЯ ПОДДЕЛКИ")
    print("="*50)
    
    print("\nПытаемся изменить данные во втором блоке...")
    # Изменяем данные во втором блоке (индекс 1)
    blockchain.chain[1].data = "ИЗМЕНЕННЫЕ ДАННЫЕ (ПОДДЕЛКА)"
    
    # Снова проверяем целостность
    is_valid, message = blockchain.is_chain_valid()
    print(f"Результат после подделки: {'✅ Цепочка валидна' if is_valid else '❌ ' + message}")

if __name__ == "__main__":
    main()
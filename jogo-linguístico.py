import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import os

# ==================== CONFIGURAÇÕES DO JOGO ====================
duration = 6  # segundos de gravação (aumentado de 4 para 6)
sample_rate = 44100

# Dicionário de palavras por nível de dificuldade
words_by_level = {
    "fácil": {
        "gato": "cat", "cachorro": "dog", "leite": "milk",
        "sol": "sun", "lua": "moon", "água": "water", "fogo": "fire",
        "terra": "earth", "vento": "wind", "livro": "book", "mesa": "table",
        "cadeira": "chair", "porta": "door", "janela": "window"
    },
    "médio": {
        "casa": "house", "escola": "school", "amigo": "friend", "amarelo": "yellow",
        "verde": "green", "azul": "blue", "vermelho": "red", "preto": "black",
        "branco": "white", "computador": "computer", "telefone": "phone", "carro": "car",
        "ônibus": "bus", "trabalho": "work"
    },
    "difícil": {
        "tecnologia": "technology", "universidade": "university",
        "pronúncia": "pronunciation", "ambiente": "environment",
        "oportunidade": "opportunity", "desenvolvimento": "development", "responsabilidade": "responsibility", "conhecimento": "knowledge",
        
    },
    "insano": {
        "autonomia": "autonomy", "metodologia": "methodology", "epistemologia": "epistemology",
        "fenomenologia": "phenomenology", "hermenêutica": "hermeneutics", "dialética": "dialectics",
        "ontologia": "ontology", "cosmologia": "cosmology", "antropologia": "anthropology",
        "sociologia": "sociology", "psicologia": "psychology", "filosofia": "philosophy",
        "biologia": "biology", "ecologia": "ecology", "arqueologia": "archaeology", "pneumonia": "pneumonia"
    },
    "lunático": {
        "interdisciplinaridade": "interdisciplinarity", "transdisciplinaridade": "transdisciplinarity",
        "multidisciplinaridade": "multidisciplinarity", "hipopotomonstrosesquipedaliofobia": "hippopotomonstrosesquipedaliophobia",
        "pneumoultramicroscopicsilicovolcanoconiose": "pneumonoultramicroscopicsilicovolcanoconiosis", "anticonstitucionalissimamente": "anticonstitutionally",
        "inconstitucionalissimamente": "unconstitutionally", "floccinaucinihilipilificação": "floccinaucinihilipilification", "pseudopseudohypoparathyroidismo": "pseudopseudohypoparathyroidism",
    }
}

# Progressão de dificuldade baseada no nível inicial
difficulty_progression = {
    "fácil": ["fácil", "médio", "difícil"],
    "médio": ["médio", "difícil", "insano"],
    "difícil": ["difícil", "insano", "lunático"]
}

level_names = {
    "fácil": "FÁCIL", "médio": "MÉDIO", "difícil": "DIFÍCIL", "insano": "INSANO", "lunático": "LUNÁTICO"
}

level_emojis = {
    "fácil": "🟢", "médio": "🟡", "difícil": "🔴", "insano": "💜", "lunático": "🌪️"
}

# Idiomas disponíveis para o modo Roguelike
available_languages = {
    "pt": "Português",
    "en": "Inglês",
    "es": "Espanhol",
    "fr": "Francês",
    "de": "Alemão"
}

# ==================== MENU PRINCIPAL ====================

def main_menu():
    """Menu principal para escolher o modo de jogo"""
    show_title()
    
    print("""
    🎮 ESCOLHA O MODO DE JOGO:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [1] 🎯 CLÁSSICO
        • Escolha sua dificuldade inicial
        • 5 perguntas por nível
        • 3 erros = Game Over
    
    [2] 🔤 COMPLETO
        • Use TODAS as palavras de cada nível
        • Só avanza após completar cada nível
        • Começa no fácil → médio → difícil
        • Mais desafiador!
    
    [3] 🎲 ROGUELIKE
        • Palavras aleatórias de qualquer nível
        • Escolha o idioma de origem
        • Bônus de pontos por sequência
        • Um novo desafio a cada partida!
    
    [4] 🚪 SAIR
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    while True:
        choice = input("👉 Escolha (1/2/3/4): ").strip()
        
        if choice == "1":
            play_classic()
            break
        elif choice == "2":
            play_complete()
            break
        elif choice == "3":
            play_roguelike()
            break
        elif choice == "4":
            print("\n👋 Obrigado por jogar! Até mais!\n")
            break
        else:
            print("❌ Opção inválida! Digite 1, 2, 3 ou 4.")

# ==================== MODO CLÁSSICO ====================

def play_classic():
    """Modo clássico original"""
    print("\n" + "="*50)
    print("   🎯 MODO CLÁSSICO")
    print("="*50 + "\n")
    
    show_rules()
    start_difficulty = choose_difficulty()
    
    print(f"\n🎮 Iniciando no nível {level_names[start_difficulty].lower()}...")
    input("   Pressione ENTER para começar...")
    
    score = 0
    wrong_answers = 0
    max_wrong = 3
    question_num = 0
    used_words = {level: [] for level in words_by_level.keys()}
    
    while wrong_answers < max_wrong:
        question_num += 1
        current_level = get_current_level(question_num, start_difficulty)
        
        available_words = {k: v for k, v in words_by_level[current_level].items() 
                         if k not in used_words[current_level]}
        
        if not available_words:
            used_words[current_level] = []
            available_words = words_by_level[current_level]
        
        pt_word = random.choice(list(available_words.keys()))
        en_answer = available_words[pt_word]
        used_words[current_level].append(pt_word)
        
        if os.path.exists("output.wav"):
            os.remove("output.wav")
        
        level_display = level_names[current_level].upper()
        level_emoji = level_emojis.get(current_level, "🎯")
        
        print(f"\n{'='*50}")
        print(f"📝 PERGUNTA #{question_num}")
        print(f"   {level_emoji} Nível: {level_display} | ❌ {wrong_answers}/3 | 🏆 {score} pts")
        print(f"{'='*50}")
        print(f"\n   �🇧  Palavra: {en_answer.upper()}")
        print(f"\n   🇧🇷  Diga a tradução em PORTUGUÊS!")
        
        record_audio()
        user_answer = recognize_speech()
        
        if user_answer is None:
            print("\n❌ Não entendi! Tente falar mais claramente.")
            wrong_answers += 1
            print(f"   Vida perdida! ({wrong_answers}/3)")
        elif user_answer == pt_word:  # Comparar com a resposta portuguesa
            score += 10
            print(f"\n✅ CORRETO! ✅")
            print(f"   '{en_answer}' = '{pt_word}' ✓")
            print(f"   +10 pontos! (Total: {score})")
        else:
            wrong_answers += 1
            print(f"\n❌ ERRADO! ❌")
            print(f"   '{en_answer}' = '{pt_word}'")
            print(f"   Você disse: '{user_answer}'")
            print(f"   Vida perdida! ({wrong_answers}/3)")
        
        # Pausa para o jogador ver o resultado
        print("\n⏳ Próxima pergunta em 3 segundos...")
        import time
        time.sleep(3)
        
        next_level = get_current_level(question_num + 1, start_difficulty)
        current_level_idx = difficulty_progression[start_difficulty].index(current_level)
        next_level_idx = difficulty_progression[start_difficulty].index(next_level)
        
        if next_level_idx > current_level_idx:
            print(f"\n{'🚀'*15}")
            print(f"   🚀 SUBINDO PARA O NÍVEL {level_names[next_level].upper()}! 🚀")
            print(f"{'🚀'*15}")
    
    show_game_over(score, question_num, start_difficulty)

# ==================== MODO COMPLETO ====================

def play_complete():
    """Modo completo - usa todas as palavras de cada nível"""
    print("\n" + "="*50)
    print("   🔤 MODO COMPLETO")
    print("="*50 + "\n")
    
    print("""
    📋 REGRAS DO MODO COMPLETO:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Você deve usar TODAS as palavras de cada nível
    • Só avança para o próximo nível após completar o atual
    • Começa no FÁCIL → MÉDIO → DIFÍCIL
    • 3 erros = Game Over
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    input("   Pressione ENTER para começar...")
    
    # Progressão fixa: fácil → médio → difícil
    progression = ["fácil", "médio", "difícil"]
    
    score = 0
    wrong_answers = 0
    max_wrong = 3
    total_questions = 0
    
    for level_index, current_level in enumerate(progression):
        level_words = list(words_by_level[current_level].items())
        random.shuffle(level_words)  # Embaralha a ordem
        
        level_name = level_names[current_level].upper()
        level_emoji = level_emojis[current_level]
        
        print(f"\n{'🔷'*25}")
        print(f"   {level_emoji} NÍVEL {level_name} - {len(level_words)} PALAVRAS")
        print(f"{'🔷'*25}")
        
        for pt_word, en_answer in level_words:
            if wrong_answers >= max_wrong:
                break
            
            total_questions += 1
            
            if os.path.exists("output.wav"):
                os.remove("output.wav")
            
            print(f"\n{'='*50}")
            print(f"📝 {total_questions}° palavra | ❌ {wrong_answers}/3 | 🏆 {score} pts")
            print(f"{'='*50}")
            print(f"\n   �🇧  Palavra: {en_answer.upper()}")
            print(f"\n   🇧🇷  Diga a tradução em PORTUGUÊS!")
            
            record_audio()
            user_answer = recognize_speech()
            
            if user_answer is None:
                print("\n❌ Não entendi!")
                wrong_answers += 1
                print(f"   Vida perdida! ({wrong_answers}/3)")
            elif user_answer == pt_word:  # Comparar com a resposta portuguesa
                score += 10
                print(f"\n✅ CORRETO! ✅")
                print(f"   '{en_answer}' = '{pt_word}' ✓")
                print(f"   +10 pontos!")
            else:
                wrong_answers += 1
                print(f"\n❌ ERRADO! ❌")
                print(f"   '{en_answer}' = '{pt_word}'")
                print(f"   Você disse: '{user_answer}'")
                print(f"   Vida perdida! ({wrong_answers}/3)")
            
            # Pausa para o jogador ver o resultado
            print("\n⏳ Próxima pergunta em 3 segundos...")
            import time
            time.sleep(3)
        
        if wrong_answers >= max_wrong:
            break
        
        # Feedback entre níveis
        if level_index < len(progression) - 1:
            next_level = progression[level_index + 1]
            print(f"\n{'🎉'*20}")
            print(f"   ✅ NÍVEL {level_name} COMPLETO!")
            print(f"   🚀 Próximo: {level_names[next_level].upper()}")
            print(f"{'🎉'*20}")
            input("\n   Pressione ENTER para continuar...")
    
    # Resultado final
    final_level = progression[min(level_index, len(progression) - 1)]
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                    GAME OVER!                              ║
    ╚══════════════════════════════════════════════════════════╝
    
    📊 RESULTADO FINAL (MODO COMPLETO):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Palavras respondidas: {total_questions}
    • Pontuação final: {score} pontos
    • Nível alcançado: {level_names[final_level].upper()}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    {"🏆 IMPRESSIONANTE! Você completou o modo completo!" if total_questions >= 40 else "💪 Bom esforço!"}
    
    Obrigado por jogar! 🎮
    """)

# ==================== MODO ROGUELIKE ====================

def choose_language():
    """Permite escolher o idioma de origem"""
    print("""
    🌐 ESCOLHA O IDIOMA DE ORIGEM:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    for i, (code, name) in enumerate(available_languages.items(), 1):
        print(f"    [{i}] {name}")
    
    print("\n")
    
    while True:
        choice = input("👉 Escolha (1/2/3/4/5): ").strip()
        
        lang_map = {"1": "pt", "2": "en", "3": "es", "4": "fr", "5": "de"}
        if choice in lang_map:
            return lang_map[choice]
        else:
            print("❌ Opção inválida!")

def play_roguelike():
    """Modo roguelike - palavras aleatórias de qualquer nível"""
    print("\n" + "="*50)
    print("   🎲 MODO ROGUELIKE")
    print("="*50 + "\n")
    
    # Escolher idioma
    source_lang = choose_language()
    lang_name = available_languages[source_lang]
    
    print(f"""
    📋 REGRAS DO MODO ROGUELIKE:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Palavras vindas de qualquer nível (aleatório)
    • Idioma de origem: {lang_name}
    • Acertos em sequência = bônus de pontos!
    • 3 erros = Game Over
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    input("   Pressione ENTER para começar...")
    
    # Criar pool de todas as palavras
    all_words = []
    for level, words in words_by_level.items():
        for pt, en in words.items():
            all_words.append((pt, en, level))
    
    random.shuffle(all_words)
    
    score = 0
    wrong_answers = 0
    max_wrong = 3
    streak = 0
    question_num = 0
    
    while wrong_answers < max_wrong and question_num < len(all_words):
        question_num += 1
        
        pt_word, en_answer, word_level = all_words[question_num - 1]
        
        if os.path.exists("output.wav"):
            os.remove("output.wav")
        
        level_emoji = level_emojis[word_level]
        
        print(f"\n{'='*50}")
        print(f"📝 PERGUNTA #{question_num}")
        print(f"   {level_emoji} Nível: {level_names[word_level].upper()}")
        print(f"   🔥 Sequência: {streak} | ❌ {wrong_answers}/3 | 🏆 {score} pts")
        print(f"{'='*50}")
        print(f"\n   🌐 Palavra ({lang_name}): {en_answer.upper()}")
        print(f"\n   🇧🇷  Diga a tradução em PORTUGUÊS!")
        
        record_audio()
        user_answer = recognize_speech()
        
        if user_answer is None:
            print("\n❌ Não entendi!")
            wrong_answers += 1
            streak = 0  # Reset da sequência
            print(f"   Vida perdida! ({wrong_answers}/3)")
        elif user_answer == en_answer:
            streak += 1
            bonus = min(streak * 2, 10)  # Bônus máx de 10 por sequência
            points = 10 + bonus
            score += points
            
            print(f"\n✅ CORRETO! ✅")
            print(f"   '{en_answer}' = '{pt_word}' ✓")
            print(f"   +{points} pontos! (10 base + {bonus} bônus sequência)")
        else:
            wrong_answers += 1
            streak = 0  # Reset da sequência
            print(f"\n❌ ERRADO! ❌")
            print(f"   '{en_answer}' = '{pt_word}'")
            print(f"   Você disse: '{user_answer}'")
            print(f"   Vida perdida! ({wrong_answers}/3)")
        
        # Pausa para o jogador ver o resultado
        print("\n⏳ Próxima pergunta em 3 segundos...")
        import time
        time.sleep(3)
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                    GAME OVER!                              ║
    ╚══════════════════════════════════════════════════════════╝
    
    📊 RESULTADO FINAL (ROGUELIKE):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Palavras respondidas: {question_num}
    • Maior sequência: {streak}
    • Pontuação final: {score} pontos
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    {"🎲 LENDÁRIO! Você é um mestre das línguas!" if score >= 200 else "👍 Boa partida!"}
    
    Obrigado por jogar! 🎮
    """)

# ==================== FUNÇÕES AUXILIARES ====================

def show_title():
    """Exibe o título do jogo com arte ASCII"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🇧🇷  PORTUGUESE TRANSLATION CHALLENGE  🇬🇧           ║
    ║                                                          ║
    ║        Leia a palavra em PORTUGUÊS e diga               ║
    ║           a tradução em INGLÊS!                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def show_rules():
    """Exibe as regras do jogo"""
    print("""
    📋 REGRAS DO JOGO:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Você verá uma palavra em PORTUGUÊS
    • Diga a tradução em INGLÊS corretamente
    • Cada acerto = +10 pontos
    • 3 erros = GAME OVER!
    • A cada 5 perguntas, o nível sobe
    • Escolha seu nível inicial no início
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

def choose_difficulty():
    """Permite ao jogador escolher a dificuldade inicial"""
    print("""
    🎯 ESCOLHA SUA DIFICULDADE INICIAL:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [1] 🟢 FÁCIL      - Para iniciantes
         → Progressão: FÁCIL → MÉDIO → DIFÍCIL
    
    [2] 🟡 MÉDIO      - Para quem já sabe um pouco
         → Progressão: MÉDIO → DIFÍCIL → INSANO
    
    [3] 🔴 DIFÍCIL   - Para experts em português
         → Progressão: DIFÍCIL → INSANO → LUNÁTICO
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    while True:
        choice = input("👉 Escolha (1/2/3): ").strip()
        
        if choice == "1":
            return "fácil"
        elif choice == "2":
            return "médio"
        elif choice == "3":
            return "difícil"
        else:
            print("❌ Opção inválida! Digite 1, 2 ou 3.")

def record_audio():
    """Grava áudio do usuário"""
    print("\n🎤 Gravando... Diga a tradução em PORTUGUÊS!")
    print("   (Fale claramente após o bip...)\n")
    
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16")
    sd.wait()
    
    wav.write("output.wav", sample_rate, recording)
    print("✅ Gravação concluída!")

def recognize_speech():
    """Reconhece a fala do usuário"""
    recognizer = sr.Recognizer()
    
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
        
        try:
            # Tenta reconhecer em português primeiro
            text = recognizer.recognize_google(audio, language="pt-BR")
            return text.lower().strip()
        except sr.UnknownValueError:
            try:
                # Fallback para inglês se não entender português
                text = recognizer.recognize_google(audio, language="en-US")
                return text.lower().strip()
            except sr.UnknownValueError:
                return None
        except sr.RequestError as e:
            print(f"❌ Erro no serviço: {e}")
            return None

def get_current_level(question_num, start_difficulty):
    """Retorna o nível atual baseado no número de perguntas e dificuldade inicial"""
    progression = difficulty_progression[start_difficulty]
    stage = (question_num - 1) // 5  # A cada 5 perguntas muda o nível
    
    if stage >= len(progression):
        stage = len(progression) - 1
    
    return progression[stage]

def show_game_over(score, questions, start_difficulty):
    """Mostra tela de fim de jogo"""
    final_level = get_current_level(questions, start_difficulty)
    final_level_name = level_names[final_level].upper()
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                    GAME OVER!                              ║
    ╚══════════════════════════════════════════════════════════╝
    
    📊 RESULTADO FINAL:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Nível inicial: {level_names[start_difficulty].upper()}
    • Nível alcançado: {final_level_name}
    • Perguntas respondidas: {questions}
    • Pontuação final: {score} pontos
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    {"🏆 EXCELENTE! Você é um gênio!" if score >= 150 else "👍 Bom trabalho!" if score >= 100 else "💪 Continue praticando!"}
    
    Obrigado por jogar! 🎮
    """)

# ==================== INÍCIO DO JOGO ====================
if __name__ == "__main__":
    main_menu()

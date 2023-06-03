from setup import Setup
from genetic import Genetic
from firefly import FireFly
from firefly2 import FireFly2
from prepare_gif import PrepareGif


if __name__ == '__main__':
    print('ARiGv4')
    setup = {
        'egg': Setup(),
        'shf': Setup(),
        'ras': Setup(),
        'ack': Setup(),
        'him': Setup()
    }
    setup['egg'].set_adaptation("inverted_egg_holder")
    setup['egg'].set_ranges(-512, 512)
    setup['shf'].set_adaptation("inverted_shf_2")
    setup['shf'].set_ranges(-100, 100)
    setup['ras'].set_adaptation("inverted_ras")
    setup['ras'].set_ranges(-5.12, 5.12)
    setup['ack'].set_adaptation("inverted_ackley")
    setup['ack'].set_ranges(-5, 5)
    setup['him'].set_adaptation("inverted_him")
    setup['him'].set_ranges(-5, 5)
    for adapt_func in setup.keys():
        setup[adapt_func].create_animal_list(1000)
        print(f"Launching setup '{adapt_func}' with algorithm Genetic()")
        genetic_task = Genetic()
        genetic_task.load_setup(setup[adapt_func])
        genetic_task.execute(10)
        history_gen = genetic_task.get_history()
        setup[adapt_func].create_animal_list(1000)
        print(f"Launching setup '{adapt_func}' with algorithm FireFly()")
        firefly_task = FireFly()
        firefly_task.load_setup(setup[adapt_func])
        firefly_task.execute(10000)
        history_ff = firefly_task.get_history()
        setup[adapt_func].create_animal_list(1000)
        print(f"Launching setup '{adapt_func}' with algorithm FireFly2()")
        firefly2_task = FireFly2()
        firefly2_task.load_setup(setup[adapt_func])
        firefly2_task.execute(7000)
        history_ff2 = firefly2_task.get_history()
        gif_writer = PrepareGif()
        gif_writer.load_setup(setup[adapt_func])
        gif_writer.load_history(history_gen)
        gif_writer.save_image(f"{adapt_func}", "genetic")
        gif_writer.load_history(history_ff)
        gif_writer.save_image(f"{adapt_func}", "firefly")
        gif_writer.load_history(history_ff2)
        gif_writer.save_image(f"{adapt_func}", "firefly2")

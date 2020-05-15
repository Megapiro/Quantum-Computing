figure1 = plot_bloch_vector([1, 0, 0], title="zeroket")
figure1.savefig('zeroket.png')

figure2 = plot_bloch_vector([-1, 0, 0], title="oneket")
figure2.savefig('oneket.png')

figure3 = plot_bloch_vector([0, 1, 0], title="xket")
figure3.savefig('xket.png')

figure4 = plot_bloch_vector([0, 0, y], title="yket")
figure4.savefig('yket.png')

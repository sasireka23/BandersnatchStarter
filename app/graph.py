from altair import Chart
import altair as alt


def chart(df, x, y, target) -> Chart:
    area_chart = Chart(df).mark_point(filled=True).encode(
        x=x, y=y,
        color=alt.Color('Rarity'),
        size=alt.value(100)

    ).properties(
        title="{x} vs {y} for {target}".format(x=x, y=y, target=target),
        background='black',
        width=500,
        height=500
    ).configure_axis(
        labelColor='white',
        titleColor='white',
        labelFontSize=16

    ).configure_title(
        color='white',
        fontSize=20
    ).configure_legend(
        labelColor='white'
    )
    area_chart.show()
    return area_chart




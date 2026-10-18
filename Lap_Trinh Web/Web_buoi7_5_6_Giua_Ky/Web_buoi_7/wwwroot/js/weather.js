$(function () {
    const storageKey = 'weatherFavorites';

    function loadFavorites() {
        const data = localStorage.getItem(storageKey);
        return data ? JSON.parse(data) : [];
    }

    function saveFavorites(favorites) {
        localStorage.setItem(storageKey, JSON.stringify(favorites));
    }

    function normalizeCity(city) {
        return city.trim().toLowerCase();
    }

    function getFavoriteCities() {
        return loadFavorites().map(normalizeCity);
    }

    function updateCardFavoriteState(card) {
        const favorites = getFavoriteCities();
        const city = normalizeCity(card.attr('data-city') || '');
        const isFavorite = favorites.includes(city);
        card.attr('data-favorite', isFavorite);
        const button = card.find('.favorite-btn');
        button.toggleClass('btn-warning', isFavorite);
        button.toggleClass('btn-outline-light', !isFavorite);
        button.toggleClass('favorite', isFavorite);
        button.find('.favorite-icon').text(isFavorite ? '★' : '☆');
        button.find('.favorite-label').text(isFavorite ? 'Đã yêu thích' : 'Yêu thích');
    }

    function sortWeatherCards() {
        const favorites = getFavoriteCities();
        const wrappers = $('#weatherCards .weather-card-wrapper').get();

        wrappers.sort((a, b) => {
            const aCity = normalizeCity($(a).attr('data-city') || '');
            const bCity = normalizeCity($(b).attr('data-city') || '');
            const aFav = favorites.includes(aCity);
            const bFav = favorites.includes(bCity);

            if (aFav !== bFav) {
                return aFav ? -1 : 1;
            }

            return aCity.localeCompare(bCity, 'vi');
        });

        $('#weatherCards').append(wrappers);
    }

    function moveSearchFavoriteCardsIntoCards() {
        $('#weatherResult .weather-card-wrapper[data-favorite="true"]').each(function () {
            const wrapper = $(this);
            const city = normalizeCity(wrapper.attr('data-city') || '');
            const exists = $('#weatherCards .weather-card-wrapper').filter(function () {
                return normalizeCity($(this).attr('data-city') || '') === city;
            }).length > 0;

            if (!exists) {
                wrapper.show();
                updateCardFavoriteState(wrapper);
                $('#weatherCards').prepend(wrapper);
            } else {
                const existing = $('#weatherCards .weather-card-wrapper').filter(function () {
                    return normalizeCity($(this).attr('data-city') || '') === city;
                }).first();
                updateCardFavoriteState(existing);
            }
        });
    }

    function restoreDefaultList() {
        moveSearchFavoriteCardsIntoCards();
        $('#weatherCards').show();
        $('#weatherCards .weather-card-wrapper').show();
        $('#weatherResult').hide().empty();
        sortWeatherCards();
    }

    function saveFavorite(city, shouldFavorite) {
        const favorites = getFavoriteCities();
        const normalized = normalizeCity(city);
        const index = favorites.indexOf(normalized);
        if (shouldFavorite && index === -1) {
            favorites.push(normalized);
        } else if (!shouldFavorite && index !== -1) {
            favorites.splice(index, 1);
        }
        saveFavorites(favorites);
    }

    $(document).on('click', '.favorite-btn', function () {
        const button = $(this);
        const wrapper = button.closest('.weather-card-wrapper');
        const city = wrapper.attr('data-city') || '';
        const favorites = getFavoriteCities();
        const normalized = normalizeCity(city);
        const isFavorite = !favorites.includes(normalized);
        saveFavorite(city, isFavorite);
        updateCardFavoriteState(wrapper);
        if ($('#cityInput').val().toString().trim()) {
            // Keep the current result visible, but keep existing favorite state
            return;
        }
        sortWeatherCards();
    });

    $('#cityInput').on('input', function () {
        if (!$(this).val().toString().trim()) {
            restoreDefaultList();
        }
    });

    $('#searchForm').on('submit', function (e) {
        e.preventDefault();
        const city = $('#cityInput').val();
        if (!city) {
            $('#weatherResult').html('<div class="alert alert-warning">Vui lòng nhập tên thành phố.</div>');
            return;
        }
        $.post('/Weather/Search', { city: city })
            .done(function (html) {
                const tempElement = $('<div/>').html(html);
                const newWrapper = tempElement.find('.weather-card-wrapper');
                const cityName = newWrapper.attr('data-city');
                if (!cityName) {
                    $('#weatherResult').html('<div class="alert alert-danger">Weather not found</div>');
                    return;
                }

                $('#weatherCards').hide();
                $('#weatherResult').empty().append(newWrapper).show();
                updateCardFavoriteState(newWrapper);
                $('#weatherResult').prepend('<div class="alert alert-success">Kết quả tìm kiếm hiển thị thành phố bạn vừa nhập.</div>');
            })
            .fail(function () {
                $('#weatherResult').html('<div class="alert alert-danger">Weather not found</div>');
            });
    });

    $('#weatherCards .weather-card-wrapper').each(function () {
        updateCardFavoriteState($(this));
    });

    sortWeatherCards();
});

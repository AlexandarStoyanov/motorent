from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from accounts.views import register, profile, my_bookings
from booking import views as booking_views


from config.views import home
from catalog.views import rent, accessories
from catalog.api import MotorcycleViewSet, AccessoryViewSet
from catalog import admin_views
from booking.views import BookingViewSet
from tours.views import tours
from tours.api import TourViewSet, send_tour_inquiry

router = DefaultRouter()
router.register("motorcycles", MotorcycleViewSet, basename="motorcycle")
router.register("accessories", AccessoryViewSet, basename="accessory")
router.register("bookings", BookingViewSet, basename="booking")
router.register("tours", TourViewSet, basename="tour")

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("api/tours/inquiry/", send_tour_inquiry, name="send_tour_inquiry"),
    path("api/", include(router.urls)),
    path("payment-success/", booking_views.booking_payment_success, name="booking_payment_success"),
    path("payment-cancel/", booking_views.booking_payment_cancel, name="booking_payment_cancel"),

    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login",),
    path("logout/",auth_views.LogoutView.as_view(next_page="/"),name="logout",),

    path("dashboard/admin/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/users/", admin_views.admin_users, name="admin_users"),
    path("dashboard/admin/users/<int:pk>/edit/", admin_views.admin_edit_user, name="admin_edit_user"),
    path("dashboard/admin/users/<int:pk>/delete/", admin_views.admin_delete_user, name="admin_delete_user"),

    path("dashboard/admin/motorcycles/", admin_views.admin_motorcycles, name="admin_motorcycles"),
    path("dashboard/admin/motorcycles/add/", admin_views.admin_add_motorcycle, name="admin_add_motorcycle"),
    path("dashboard/admin/motorcycles/<int:pk>/delete/", admin_views.admin_delete_motorcycle, name="admin_delete_motorcycle"),
    path("dashboard/admin/motorcycles/<int:pk>/edit/", admin_views.admin_edit_motorcycle, name="admin_edit_motorcycle"),

    path("dashboard/admin/accessories/", admin_views.admin_accessories, name="admin_accessories"),
    path("dashboard/admin/accessories/add/", admin_views.admin_add_accessory, name="admin_add_accessory"),
    path("dashboard/admin/accessories/<int:pk>/delete/", admin_views.admin_delete_accessory, name="admin_delete_accessory"),
    path("dashboard/admin/accessories/<int:pk>/edit/", admin_views.admin_edit_accessory, name="admin_edit_accessory"),

    path("dashboard/admin/bookings/", admin_views.admin_bookings, name="admin_bookings"),
    path("dashboard/admin/bookings/<int:pk>/delete/",admin_views.admin_delete_booking,name="admin_delete_booking"),

    path("dashboard/admin/discount-codes/", admin_views.admin_discount_codes, name="admin_discount_codes"),
    path("dashboard/admin/discount-codes/add/", admin_views.admin_add_discount_code, name="admin_add_discount_code"),
    path("dashboard/admin/discount-codes/<int:pk>/delete/", admin_views.admin_delete_discount_code, name="admin_delete_discount_code"),

    path("dashboard/admin/reviews/", admin_views.admin_reviews, name="admin_reviews"),
    path("dashboard/admin/reviews/add/", admin_views.admin_add_review, name="admin_add_review"),
    path("dashboard/admin/reviews/<int:pk>/delete/", admin_views.admin_delete_review, name="admin_delete_review"),

    path("dashboard/admin/tours/", admin_views.admin_tours, name="admin_tours"),
    path("dashboard/admin/tours/add/", admin_views.admin_add_tour, name="admin_add_tour"),
    path("dashboard/admin/tours/<int:pk>/edit/", admin_views.admin_edit_tour, name="admin_edit_tour"),
    path("dashboard/admin/tours/<int:pk>/delete/", admin_views.admin_delete_tour, name="admin_delete_tour"),
]

urlpatterns += i18n_patterns(
    path("", home, name="home"),
    path("rent/", rent, name="rent"),
    path("tours/", tours, name="tours"),
    path("accessories/", accessories, name="accessories"),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)